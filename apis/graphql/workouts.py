import graphene
from graphene_django import DjangoObjectType
from graphene import Field, List, ID, String, Date
from ..models import Workout
# from core.models import Profile


class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout
        fields = "__all__"


class Query(graphene.ObjectType):
    all_workouts = List(WorkoutType)
    workout_by_id = Field(WorkoutType, id=ID(required=True))
    workouts_by_profile = List(WorkoutType, profile_id=ID(required=False))

    def resolve_all_workouts(root, info):
        return Workout.objects.all()

    def resolve_workout_by_id(root, info, id):
        return Workout.objects.get(id=id)

    def resolve_workouts_by_profile(root, info, profile_id):
        return Workout.get_profile_workouts(profile_id)


class CreateWorkout(graphene.Mutation):
    class Arguments:
        title = String(required=True)
        date = Date(required=True)
        notes = String()
        workout_type = String()

    workout = Field(WorkoutType)

    # @classmethod
    def mutate(self, info, title, date, notes=None, workout_type="strength", profile = None):
        workout = Workout.objects.create(
            title=title,
            date=date,
            notes=notes,
            workout_type=workout_type,
        )
        return CreateWorkout(workout=workout)


class Mutation(graphene.ObjectType):
    create_workout = CreateWorkout.Field()
