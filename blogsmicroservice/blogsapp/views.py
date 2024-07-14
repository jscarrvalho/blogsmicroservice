from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from blogsmicroservice.blogsapp.models import BlogPost
from rest_framework import viewsets, status
from blogsmicroservice.blogsapp.serializers import BlogPostSerializer
from .permissions import IsAuthenticatedForManipulateResource


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(deleted_at__isnull=True).order_by('-date_posted')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedForManipulateResource]

    def destroy(self, request, *args, **kwargs):
        blog_post = self.get_object()
        blog_post.deleted_at = timezone.now()
        blog_post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


signup_signin_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    },
    required=['username', 'password']
)

signup_signin_response_body_ok = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'token': openapi.Schema(type=openapi.TYPE_STRING, description='token basic auth to be used'),
    }
)

signup_signin_response_body_error = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
    }
)

signup_signin_responses = {
    status.HTTP_200_OK: signup_signin_response_body_ok,
    status.HTTP_400_BAD_REQUEST: signup_signin_response_body_error
}


@swagger_auto_schema(method='post', request_body=signup_signin_request_body, responses=signup_signin_responses)
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    elif not username or not password:
        return Response({'error': 'Username or password cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='post', request_body=signup_signin_request_body, responses=signup_signin_responses)
@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
