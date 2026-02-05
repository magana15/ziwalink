import graphene
from graphene_django import DjangoObjectType
from .models import ZiwaUser

from .models import Post, Comment, Like, Share


class UserType(DjangoObjectType):
    class Meta:
        model = ZiwaUser
        fields = ("id", "username")


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
