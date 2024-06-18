import graphene
from myapp import models

class Query(graphene.ObjectType):
    pass


for table_name, graphql_type in models.graphql_types.items():
    def make_resolver(graphql_type):
        def resolve_dynamic_model(self, info, **kwargs):
            filters = {key: value for key, value in kwargs.items() if value is not None}
            return graphql_type._meta.model.objects.filter(**filters)
        return resolve_dynamic_model

    args = {
        field.name: graphene.String() for field in graphql_type._meta.model._meta.fields
    }

    resolve_func = make_resolver(graphql_type)
    field_name = table_name.lower()

    Query._meta.fields[field_name] = graphene.Field(graphene.List(graphql_type), resolver=resolve_func, args=args)
    print(f"Added field '{field_name}' to Query with type {graphql_type}")


schema = graphene.Schema(query=Query, types=list(models.graphql_types.values()))