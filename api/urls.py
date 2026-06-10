from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'))
]

router = DefaultRouter()
router.register(r'api/users', views.UserAPI, basename='blog_users')
router.register(r'api/posts', views.BlogPostAPI, basename='blog_posts')
router.register(r'api/comments', views.CommentAPI, basename='users_comments')
router.register(r'api/likes', views.LikeAPI, basename='users_likes')
urlpatterns += router.urls
