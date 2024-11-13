import yaml
import os
from django.db import models
import graphene
from graphene_django import DjangoObjectType
from dynamic_schema_graphql.settings import BASE_DIR

schema_path = os.path.join(BASE_DIR, "etc", "schema.yaml")
with open(schema_path, "r") as file:
    schema_yaml = yaml.safe_load(file)

graphql_types = {}

for table in schema_yaml['tables']:
    attrs = {
        '__module__': __name__,
        'Meta': type('Meta', (), {'db_table': table['name'], 'managed': False})
    }
    graphql_attrs = {
        '__module__': __name__
    }

    primary_key_set = False
    for field in table['fields']:
        field_type = field['type']
        if field_type == 'String':
            attrs[field['name']] = models.CharField(max_length=255, primary_key=not primary_key_set)
            graphql_attrs[field['name']] = graphene.String()
        elif field_type == 'Integer':
            attrs[field['name']] = models.IntegerField(primary_key=not primary_key_set)
            graphql_attrs[field['name']] = graphene.Int()
        elif field_type == 'Date':
            attrs[field['name']] = models.DateField(primary_key=not primary_key_set)
            graphql_attrs[field['name']] = graphene.Date()
        elif field_type == 'DateTime':
            attrs[field['name']] = models.DateTimeField(primary_key=not primary_key_set)
            graphql_attrs[field['name']] = graphene.DateTime()
        elif field_type == 'Double':
            attrs[field['name']] = models.FloatField(primary_key=not primary_key_set)
            graphql_attrs[field['name']] = graphene.Float()
        primary_key_set = True

    model_name = table['name']
    model_class = type(model_name, (models.Model,), attrs)
    graphql_type = type(table['name'], (DjangoObjectType,), {
        'Meta': type('Meta', (), {'model': model_class}),
        **graphql_attrs
    })

    graphql_types[table['name']] = graphql_type
    globals()[model_name] = model_class