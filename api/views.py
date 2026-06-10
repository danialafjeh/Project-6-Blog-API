from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Category, Tag, BlogPost, Like, Comment
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    UserSerializer, 
    RegisterUserSerializer, 
    BlogPostReadSerializer, 
    BlogPostWriteSerializer, 
    CommentReadSerializer, 
    CommentWriteSerializer,
    LikeReadSerializer,
)
from django.db.models import Q

# Create your views here.

class UserAPI(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['list', 'search', 'destroy']:
            permissions = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve', 'update']: 
            permissions = [IsAuthenticated]
        elif self.action == 'create':
            permissions = [AllowAny]
        
        return [permission() for permission in permissions]
    
    def list(self, request):
        queryset = User.objects.all()
        #serializer = UserSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(User, id=pk, username=request.user.username)
        serializer = UserSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        username = request.query_params.get('username')
        queryset = User.objects.filter(username__icontains=username)
        #serializer = UserSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message':'user registered successfully',
                    'username':user.username
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        instance = get_object_or_404(User, id=pk, username=request.user.username)
        serializer = UserSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if user == request.user:
            return Response({'message':'you can not delete your own profile'}, status=status.HTTP_403_FORBIDDEN)
        elif user.is_superuser:
            return Response({'message':'you can not delete a super user'}, status=status.HTTP_403_FORBIDDEN)
        elif user.is_staff:
            return Response({'message':'you can not delete an admin user'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user.delete()
            return Response({'message':'user deleted successully'}, status=status.HTTP_200_OK)


class BlogPostAPI(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = [AllowAny]
        elif self.action in ['create', 'update', 'destroy']:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    def list(self, request):
        queryset = BlogPost.objects.all()
        #serializer = BlogPostReadSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BlogPostReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(BlogPost, id=pk)
        serializer = BlogPostReadSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        entry = request.query_params.get('about')
        queryset = BlogPost.objects.filter(
            Q(title__icontains=entry) | 
            Q(category__name__icontains=entry) |
            Q(tags__name__icontains=entry)
        ).distinct()
        #serializer = BlogPostReadSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BlogPostReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = BlogPostWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response({'message':'your post published successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        instance = get_object_or_404(BlogPost, id=pk, author=request.user)
        serializer = BlogPostWriteSerializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'your post has been updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        instance = get_object_or_404(BlogPost, id=pk, author=request.user)
        instance.delete()
        return Response({'message':'your post has been deleted'}, status=status.HTTP_200_OK)


class CommentAPI(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'delviaadmin']:
            permissions = [IsAuthenticated, IsAdminUser]
        elif self.action in ['blogpost', 'create', 'destroy']:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    def list(self, request):
        queryset = Comment.objects.all()
        #serializer = CommentReadSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)  
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(Comment, id=pk)
        serializer = CommentReadSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def blogpost(self, request):
        related_post = request.query_params.get('id')
        queryset = Comment.objects.filter(post__id=related_post)
        #serializer = CommentReadSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = CommentWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'message':'your comment has been added for this post'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        instance = get_object_or_404(Comment, id=pk, user=request.user)
        instance.delete()
        return Response({'message':'your comment has been deleted'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delviaadmin(self, request, pk):
        instance = get_object_or_404(Comment, id=pk)
        instance.delete()
        return Response({'message':'comment deleted successfully'}, status=status.HTTP_200_OK)


class LikeAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'])
    def blogpost(self, request):
        related_post = request.query_params.get('id')
        queryset = Like.objects.filter(post__id=related_post)
        #serializer = LikeReadSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = LikeReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk):
        user_like = Like.objects.filter(post__id=pk, user=request.user).first()
        if user_like:
            user_like.delete()
            return Response({'message':'you unliked this post'}, status=status.HTTP_200_OK)
        else:
            related_post = get_object_or_404(BlogPost, id=pk)
            Like.objects.create(user=request.user, post=related_post)
            return Response({'message':'you liked this post'}, status=status.HTTP_200_OK)
