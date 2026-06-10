from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions','groups')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )

        extra_kwargs = {
            'password':{
                'write_only':True
            },
            'email':{
                'required':True
            },
            'first_name':{
                'required':True
            },
            'last_name':{
                'required':True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return  user


class BlogPostReadSerializer(serializers.ModelSerializer):
    #For BlogPost list, retrieve, search methods in CRUD operations
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(slug_field='username',read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'author',
            'title',
            'content',
            'category',
            'tags',
            'created_at',
            'updated_at',
            'comments_count',
            'likes_count'
        )

        extra_kwargs = {
            'author':{
                'read_only':True
            },
            'created_at':{
                'read_only':True
            },
            'updated_at':{
                'read_only':True
            }  
        }

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class BlogPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

        extra_kwargs = {
            'author':{
                'read_only':True
            },
            'created_at':{
                'read_only':True
            },
            'updated_at':{
                'read_only':True
            }  
        }


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class BlogPostMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title')

class CommentReadSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    post = BlogPostMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

        extra_kwargs = {
            'user':{
                'read_only':True
            },
            'created_at':{
                'read_only':True
            }
        }


class LikeReadSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    post = BlogPostMiniSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
