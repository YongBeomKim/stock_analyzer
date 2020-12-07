from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router = DefaultRouter.register('posts/', PostViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router.urls))
]
