from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from task.models import Post, Comment
from task.serializers import PostSerializer, CommentSerializer


class PostListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        search = request.query_params.get('search', None)
        if search:
            posts = Post.objects.filter(title__icontains=search).order_by('_created_at')
        else:
            posts = Post.objects.all().order_by('_created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializers = PostSerializer(post)
        return Response(serializers.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if request.user != post.author:
            raise PermissionDenied("Faqat post egasi tahrirlashi mumkin.")
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if request.user != post.author:
            raise PermissionDenied("Faqat post egasi o‘chirishi mumkin.")
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)

        if request.user != comment.author and not request.user.is_staff:
            raise PermissionDenied("Faqat comment egasi yoki admin ochira oladi.")

        comment.delete()
        return Response({"message": "Delete successful completed"}, status=status.HTTP_204_NO_CONTENT)


