import graphene
from graphql_jwt.decorators import login_required
from feed.types import UserType
from graphql import GraphQLError
from users.models import ZiwaUser

class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.String(required=False)

    def mutate(self, info, username, email, password, role="FARMER"):

        # Prevent duplicate usernames
        if ZiwaUser.objects.filter(username=username).exists():
            raise GraphQLError("Username already exists")

        # Prevent duplicate email
        if ZiwaUser.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists")

        user = ZiwaUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

        return RegisterUser(user=user)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
