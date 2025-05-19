import graphene
from graphene_django import DjangoObjectType
from graphene import Field, List, ID, String, Int
from ..models import Exercise
from core.models import Profile
from graphql import GraphQLError
# from graphql_jwt.decorators import login_required


class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
        fields = "__all__"


# =======================
# Query Class
# =======================
# @login_required
class Query(graphene.ObjectType):
    all_exercises = List(ExerciseType)
    exercise_by_id = Field(ExerciseType, id=ID(required=True))
    exercises_by_profile = List(ExerciseType, profile_id=ID(required=True))

    def resolve_all_exercises(root, info):
        return Exercise.objects.all()

    def resolve_exercise_by_id(root, info, id):
        return Exercise.objects.get(id=id)

    def resolve_exercises_by_profile(root, info, profile_id):
        return Exercise.objects.filter(profile__id=profile_id)


# =======================
# Create Mutation
# =======================
class CreateExercise(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        description = String()
        duration = Int()
        profile_id = ID(required=True)

    exercise = Field(ExerciseType)

    # @classmethod
    def mutate(self, info, name, profile_id, description=None, duration=None):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise GraphQLError("Profile with the given ID does not exist.")

        exercise = Exercise.objects.create(
            name=name, description=description, duration=duration, profile=profile
        )
        return CreateExercise(exercise=exercise)


# =======================
# Mutation Class
# =======================
class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()
