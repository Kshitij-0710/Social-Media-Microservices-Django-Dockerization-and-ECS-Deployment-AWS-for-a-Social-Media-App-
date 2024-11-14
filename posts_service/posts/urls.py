# posts/urls.py
from django.urls import path
from .views import PostListCreate,PostDetailView

urlpatterns = [
    path('', PostListCreate.as_view(), name='post-list-create'),
    path('detail/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]
