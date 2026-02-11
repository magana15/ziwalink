import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from .models import Post, Comment, Like
from users.queries import UserQuery, Mutation as UserMutation
from .types import PostType, CommentType, UserType

User = get_user_model()

class Query(UserQuery,graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    def resolve_posts(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        return (
            Post.objects
            .select_related("author")
            .prefetch_related("comments__user", "likes__user")
            .all()
        )

    def resolve_post(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        return (
            Post.objects
            .select_related("author")
            .prefetch_related("comments__user", "likes__user")
            .get(pk=id)
        )

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)
        image = Upload(required=False)
        visibility = graphene.String(required=False)

    def mutate(self, info, content, visibility="public"):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        post = Post.objects.create(
            author=user,
            content=content,
            visibility=visibility
        )
        return CreatePost(post=post)


class LikePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        Like.objects.get_or_create(
            user=user,
            post_id=post_id
        )
        return LikePost(success=True)


class AddComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")

        comment = Comment.objects.create(
            user=user,
            post_id=post_id,
            content=content
        )
        return AddComment(comment=comment)
class RequestPasswordReset(graphene.Mutation):
    token = graphene.String()  # Return token to the user in demo

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError("User not found")

        # Generate a token
        token = default_token_generator.make_token(user)

        return RequestPasswordReset(token=token)

class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    def mutate(self, info, username, token, new_password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError("Invalid username")

        if not default_token_generator.check_token(user, token):
            raise GraphQLError("Invalid or expired token")

        user.set_password(new_password)
        user.save()
        return ResetPassword(success=True)

class Mutation(UserMutation,graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_post = CreatePost.Field()
    like_post = LikePost.Field()
    add_comment = AddComment.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
