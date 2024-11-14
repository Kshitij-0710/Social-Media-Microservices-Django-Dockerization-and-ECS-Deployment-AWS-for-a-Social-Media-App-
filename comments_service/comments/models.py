# comment_project/comments/models.py
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the comment
    post_id = models.IntegerField()  # The ID of the post the comment is associated with
    content = models.TextField()  # The actual text of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the comment was created

    class Meta:
        constraints = []  # Empty constraints to avoid enforcing uniqueness

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post_id}"
