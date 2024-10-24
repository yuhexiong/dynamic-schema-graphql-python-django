import graphene
from graphql_app import models
from graphql_app.filters import get_filter_argument
from django.db.models import Q 

class OrderEnum(graphene.Enum):
    ASC = "ASC"
    DESC = "DESC"

class OrderByInput(graphene.InputObjectType):
    column = graphene.String(required=True)
    order = graphene.Field(OrderEnum, required=True)


class Query(graphene.ObjectType):
    pass

def make_resolver(graphql_type):
    def resolve_dynamic_model(self, info, offset=0, limit=1000, order_by=None, filter=None, **kwargs):
        query = Q()
        if filter:
            for field, operations in filter.items():
                if operations:
                    for operation, value in operations.items():
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
        qs = graphql_type._meta.model.objects.filter(query)

        if order_by:
            order_by_fields = []
            for item in order_by:
                order = '' if item.order == OrderEnum.ASC else '-'
                order_by_fields.append(f"{order}{item.column}")
            qs = qs.order_by(*order_by_fields)

        return qs[offset:offset + limit]
    return resolve_dynamic_model

for table_name, graphql_type in models.graphql_types.items():
    args = {
        'offset': graphene.Argument(graphene.Int, default_value=0),
        'limit': graphene.Argument(graphene.Int, default_value=1000),
        'order_by': graphene.Argument(graphene.List(OrderByInput))
    }

    filter = {}
    for field in graphql_type._meta.model._meta.fields:
        filter_dict = get_filter_argument(field)  
        filter_name, filter_argument = list(filter_dict.items())[0]  
        filter[filter_name] = filter_argument

    FilterInputType = type(f"{graphql_type.__name__}FilterInput", (graphene.InputObjectType,), filter)
    args.update({'filter': graphene.Argument(FilterInputType)})

    Query._meta.fields[table_name] = graphene.Field(graphene.List(graphql_type), resolver=make_resolver(graphql_type), args=args, name=table_name)

    print(f"Added table '{table_name}' to Query with type {graphql_type}")

schema = graphene.Schema(query=Query, types=list(models.graphql_types.values()), auto_camelcase=False)
