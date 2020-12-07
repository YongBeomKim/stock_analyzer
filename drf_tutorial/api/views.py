from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Post
from .serializers import PostSerializer


# Create your views here.

# CBV (Class Based View)
class PostListAPIView(APIView):
    def get(self, request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FBV (Function Based View)
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        qs = Post.abojects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
    else:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Mixin
# CreateModelMixin
# ListModelMixin
# RetrieveModelMixin
# UpdateModelMixin
# DestroyModelMixin

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)


class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# generics APIView
# generics.CreateAPIView : 생성
# generics.ListAPIView : 목록
# generics.RetrieveAPIView : 조회
# generics.DestroyAPIView : 삭제
# generics.UpdateAPIView : 수정
# generics.RetrieveUpdateAPIView : 조회/수정
# generics.RetrieveDestroyAPIView : 조회/삭제
# generics.ListCreateAPIView : 목록/생성
# generics.RetrieveUpdateDestroyAPIView : 조회/수정/삭제

class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# ViewSet
# generics APIView에서도 queryset과 serializer_class가 공통임에도 따로 기재해야함. 이를 줄이기 위함.
# viewsets.ReadOnlyModelViewSet : 목록 조회, 특정 레코드 조회
# viewsets.ModelViewSet : 목록 조회, 특정 레코드 생성/조회/수정/삭제

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
