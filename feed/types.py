import graphene
from graphene_django import DjangoObjectType
from .models import ZiwaUser
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like, Share

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email","phone_number")


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "content", "created_at", "user")


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ("id", "user", "created_at")


class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = ("id", "user", "created_at")


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "visibility",
            "created_at",
            "image",
            "author",
            "comments",
            "likes",
            "shares",
        )
