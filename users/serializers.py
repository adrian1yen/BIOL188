from rest_framework import serializers
from posts.serializers import CommentSerializer, PostSerializer
from users import models as user_models

class ClassroomSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    teacher = serializers.CharField(source="teacher.user.username")

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    post_id = serializers.IntegerField(source='post.id')
    post_title = serializers.CharField(source='post.title')
    content = serializers.CharField()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(source='user.username')
    role = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserProfile
        fields = ('id', 'role', 'username', 'classrooms', 'comments', 'posts')

    username = serializers.CharField(source='user.username')
    classrooms = ClassroomSerializer(many=True)
    comments = CommentSerializer(many=True)
    posts = PostSerializer(many=True, required=False)
