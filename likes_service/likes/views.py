# likes/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Like

class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        # Check if the user has already liked this post
        if Like.objects.filter(user=request.user, post_id=post_id).exists():
            return Response({"detail": "Already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new like
        Like.objects.create(user=request.user, post_id=post_id)
        return Response({"detail": "Post liked"}, status=status.HTTP_201_CREATED)

class UnlikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        # Check if the user has liked this post
        try:
            like = Like.objects.get(user=request.user, post_id=post_id)
            like.delete()
            return Response({"detail": "Post unliked"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
class ListLike(APIView):
    def get(self, request, post_id):
        likes = Like.objects.filter(post_id=post_id)
        like_data = [{"user": like.user.username} for like in likes]
        return Response(like_data, status=status.HTTP_200_OK)