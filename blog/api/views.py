from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from ..models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(status='published').select_related('author')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'published_date']
    ordering_fields = ['published_date', 'title']


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(pk=post_id, status='published')
        except Post.DoesNotExist:
            raise ValidationError({"detail": "The post does not exist or is not published."})
        
        serializer.save(post=post)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
