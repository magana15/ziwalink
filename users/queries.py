import graphene
from graphql_jwt.decorators import login_required
from feed.types import UserType

class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user
