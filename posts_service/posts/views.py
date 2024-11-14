# post_project/posts/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
import requests

class PostListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        post_data = [{"title": post.title, "content": post.content, "author": post.author.username} for post in posts]
        return Response(post_data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        
        post = Post.objects.create(author=request.user, title=title, content=content)
        return Response({"post_id": post.id}, status=status.HTTP_201_CREATED)
class PostDetailView(APIView):
    def get(self, request, post_id):
        # Step 1: Fetch post details
        try:
            post = Post.objects.get(id=post_id)
            post_data = {
                "title": post.title,
                "content": post.content,
                "author": post.author.username,
                "created_at": post.created_at,
            }
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Fetch likes for the post from like_project
        try:
            likes_response = requests.get(
                f"http://localhost:8002/api/likes/list/{post_id}/"
            )
            likes_data = likes_response.json() if likes_response.status_code == 200 else []
            post_data["likes_count"] = len(likes_data)
            post_data["liked_by_users"] = [like["user"] for like in likes_data]
        except requests.RequestException:
            post_data["likes_count"] = 0
            post_data["liked_by_users"] = []

        # Step 3: Fetch comments for the post from comment_project
        try:
            comments_response = requests.get(f"http://localhost:8003/api/comments/list/{post_id}/")
            comments_data = comments_response.json() if comments_response.status_code == 200 else []
            post_data["comments"] = comments_data  # Add comments to post data
        except requests.RequestException:
            post_data["comments"] = []  # Default to empty list if comments service is unavailable

        return Response(post_data, status=200)

        # Step 4: Return aggregated data
        