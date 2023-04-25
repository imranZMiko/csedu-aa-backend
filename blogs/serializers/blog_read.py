from rest_framework import serializers
from blogs.models import Blog, Comment, Like, Tag

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        # Retrieve the user profile information for the like's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture  # Use profile_picture directly
        }

    class Meta:
        model = Like
        fields = ('id', 'user', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        # Retrieve the user profile information for the comment's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture  # Use profile_picture directly
        }

    def get_likes_count(self, obj):
        # Retrieve the count of likes on the comment
        return obj.likes.count()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'likes_count', 'created_at', 'updated_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('slug',)  # Use the 'slug' field to serialize tags

class BlogReadSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()  # Update likes_count field

    def get_user(self, obj):
        # Retrieve the user profile information for the blog's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture
        }

    def get_likes_count(self, obj):
        # Retrieve the number of likes associated with the blog
        return obj.likes.count()

    class Meta:
        model = Blog
        fields = ('id', 'user', 'title', 'tags', 'content', 'comments', 'likes', 'likes_count', 'created_at', 'updated_at', 'cover_picture') 
        read_only_fields = ('id', 'user', 'comments', 'likes', 'likes_count', 'created_at', 'updated_at')


