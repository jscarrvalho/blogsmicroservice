from django.utils import timezone
from rest_framework.response import Response

from blogsmicroservice.blogsapp.models import BlogPost
from rest_framework import permissions, viewsets, status
from blogsmicroservice.blogsapp.serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(deleted_at__isnull=True).order_by('-date_posted')
    serializer_class = BlogPostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        blog_post = self.get_object()
        blog_post.deleted_at = timezone.now()
        blog_post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)