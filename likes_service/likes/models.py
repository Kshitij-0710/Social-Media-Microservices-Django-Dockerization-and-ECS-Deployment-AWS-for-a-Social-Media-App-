# likes/models.py
from django.db import models
from django.contrib.auth.models import User  # Make sure this is consistent with auth_project's user model

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who liked the post
    post_id = models.IntegerField()  # Stores the ID of the post in post_project
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post_id')  # Prevents a user from liking the same post multiple times
