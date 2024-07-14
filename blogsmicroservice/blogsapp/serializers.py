from blogsmicroservice.blogsapp.models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.CharField(source='author.username', default='Anonymous', allow_null=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author', 'date_posted', 'updated_at']