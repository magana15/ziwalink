from django.db import models
from django.contrib.auth.models import User
from users.models import ZiwaUser

class Post(models.Model):
    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("private", "Private"),
    )

    author = models.ForeignKey(ZiwaUser, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default="public")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(ZiwaUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} on {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(ZiwaUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]
    def __str__(self):
        return f"{self.user} likes the post"

class Share(models.Model):
    user = models.ForeignKey(ZiwaUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} shared the post."
    class Meta:
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]


