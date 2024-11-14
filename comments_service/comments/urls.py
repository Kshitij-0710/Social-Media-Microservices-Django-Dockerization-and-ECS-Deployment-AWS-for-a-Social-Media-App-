# comments/urls.py
from django.urls import path
from .views import AddComment, RetrieveComments, DeleteComment

urlpatterns = [
    path('add/<int:post_id>/', AddComment.as_view(), name='add-comment'),
    path('list/<int:post_id>/', RetrieveComments.as_view(), name='list-comments'),
    path('delete/<int:comment_id>/', DeleteComment.as_view(), name='delete-comment'),
]
