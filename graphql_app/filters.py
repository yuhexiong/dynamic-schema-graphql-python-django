import graphene
from django.db import models


class FilterBetweenInput(graphene.InputObjectType):
    start = graphene.String()
    end = graphene.String()

class FilterIntInput(graphene.InputObjectType):
    equals = graphene.Int()
    greater_than = graphene.Int()
    greater_than_or_equals = graphene.Int()
    less_than = graphene.Int()
    less_than_or_equals = graphene.Int()
    between = graphene.Field(FilterBetweenInput)

class FilterFloatInput(graphene.InputObjectType):
    equals = graphene.Float()
    greater_than = graphene.Float()
    greater_than_or_equals = graphene.Float()
    less_than = graphene.Float()
    less_than_or_equals = graphene.Float()
    between = graphene.Field(FilterBetweenInput)

class FilterStringInput(graphene.InputObjectType):
    equals = graphene.String()
    contains = graphene.List(graphene.String)
    greater_than = graphene.String()
    greater_than_or_equals = graphene.String()
    less_than = graphene.String()
    less_than_or_equals = graphene.String()
    between = graphene.Field(FilterBetweenInput)

class FilterDateInput(graphene.InputObjectType):
    equals = graphene.Date()
    greater_than = graphene.Date()
    less_than = graphene.Date()
    between = graphene.Field(FilterBetweenInput)


def get_filter_argument(field):
    if isinstance(field, models.IntegerField):
        return {field.name: graphene.Argument(FilterIntInput)}
    elif isinstance(field, models.FloatField):
        return {field.name: graphene.Argument(FilterFloatInput)}
    elif isinstance(field, models.DateField) or isinstance(field, models.DateTimeField):
        return {field.name: graphene.Argument(FilterDateInput)}
    else:
        return {field.name: graphene.Argument(FilterStringInput)}