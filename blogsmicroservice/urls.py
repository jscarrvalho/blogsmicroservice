from django.urls import path, include
from rest_framework import routers, permissions
from blogsmicroservice.blogsapp import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="API documentation for the Blog API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'blogs', views.BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup', views.signup, name='signup'),
    path('auth/signin', views.signin, name='signin'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
