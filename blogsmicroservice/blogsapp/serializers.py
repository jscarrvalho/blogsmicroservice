from blogsmicroservice.blogsapp.models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'date_posted', 'updated_at']