import graphene
from graphene_django.debug import DjangoDebug
from apis.graphql import *


class Query(WorkoutQuery, StatQuery, ExerciseQuery, graphene.ObjectType):
    """
    query class for all queries that implemented in the project
    queries are used to get data from the database
    it an alternative to the REST API GET method
    the difference is that the queries are more flexible and can be used to get data from multiple models in one request
    """

    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(WorkoutMutation, StatMutation, ExerciseMutation, graphene.ObjectType):
    """
    mutation class for all mutations that implemented in the project
    mutations are used to create, update, delete data
    it an alternative to the REST API POST, PUT, DELETE methods
    the difference is that the mutations are more flexible and can be used to create, update, delete data in one request
    """

    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
