import graphene
from myapp import models
from myapp.filters import get_filter_argument
from django.db.models import Q 

class Query(graphene.ObjectType):
    pass

for table_name, graphql_type in models.graphql_types.items():
    def make_resolver(graphql_type):
        def resolve_dynamic_model(self, info, **kwargs):
            query = Q()
            for field, filters in kwargs.items():
                if filters:
                    for operation, value in filters.items():
                        if value is not None:
                            if operation == 'between':
                                query &= Q(**{f"{field}__range": (value['start'], value['end'])})
                            elif operation == 'greater_than':
                                query &= Q(**{f"{field}__gt": value})
                            elif operation == 'greater_than_or_equals':
                                query &= Q(**{f"{field}__gte": value})
                            elif operation == 'less_than':
                                query &= Q(**{f"{field}__lt": value})
                            elif operation == 'less_than_or_equals':
                                query &= Q(**{f"{field}__lte": value})
                            elif operation == 'contains':
                                query &= Q(**{f"{field}__in": value})
                            elif operation == 'equals':
                                query &= Q(**{f"{field}": value})
                            else:
                                query_key = f"{field}__{operation}"
                                query &= Q(**{query_key: value})
            return graphql_type._meta.model.objects.filter(query)
        return resolve_dynamic_model

    args = {}
    for field in graphql_type._meta.model._meta.fields:
        args.update(get_filter_argument(field))

    field_name = table_name.lower()
    Query._meta.fields[field_name] = graphene.Field(graphene.List(graphql_type), resolver=make_resolver(graphql_type), args=args)
    print(f"Added field '{field_name}' to Query with type {graphql_type}")

schema = graphene.Schema(query=Query, types=list(models.graphql_types.values()))