# likes/urls.py
from django.urls import path
from .views import ListLike, LikePost, UnlikePost  # Ensure ListLikes is included here

urlpatterns = [
    path('list/<int:post_id>/', ListLike.as_view(), name='list-likes'),
    path('like/<int:post_id>/', LikePost.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', UnlikePost.as_view(), name='unlike-post'),
]
