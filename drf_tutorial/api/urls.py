from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('viewset', views.PostViewSet)

urlpatterns = [
    path('cbv/post/', views.PostListAPIView.as_view()),
    path('cbv/post/<int:pk>/', views.PostDetailAPIView.as_view()),

    path('fbv/post/', views.post_list),
    path('fbv/post/<int:pk>/', views.post_detail),

    path('mixin/post/', views.PostListMixins.as_view()),
    path('mixin/post/<int:pk>/', views.PostDetailMixins.as_view()),

    path('generic/post/', views.PostListGenericAPIView.as_view()),
    path('generic/post/<int:pk>/', views.PostDetailGenericAPIView.as_view()),

    path('', include(router.urls)),
]
