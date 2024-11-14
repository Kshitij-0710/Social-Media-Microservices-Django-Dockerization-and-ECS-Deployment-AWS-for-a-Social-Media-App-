# comments/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Comment

class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        content = request.data.get("content")
        if not content:
            return Response({"detail": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(user=request.user, post_id=post_id, content=content)
        return Response({"detail": "Comment added", "comment_id": comment.id}, status=status.HTTP_201_CREATED)

class RetrieveComments(APIView):
    # Remove permission_classes to allow public access
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")
        comment_data = [
            {
                "user": comment.user.username,
                "content": comment.content,
                "created_at": comment.created_at
            }
            for comment in comments
        ]
        return Response(comment_data, status=200)

class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return Response({"detail": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
