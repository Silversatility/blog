from rest_framework import serializers
from ..models import Post, Comment, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created']

    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Comment content must be at least 5 characters long.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author_name', 'status', 'comments']

    def validate_title(self, value):
        if Post.objects.filter(title=value).exists():
            raise serializers.ValidationError("A post with this title already exists.")
        return value

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author']

        def validate_content(self, value):
            if len(value) < 10:
                raise serializers.ValidationError("Post content must be at least 10 characters long.")
            return value