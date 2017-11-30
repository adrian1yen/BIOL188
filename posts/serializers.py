from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(source='user.username')

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = AuthorSerializer()
    content = serializers.CharField()
    score = serializers.IntegerField()

class ClassroomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    classroom = ClassroomSerializer()
    title = serializers.CharField()
    author = AuthorSerializer()
    content = serializers.CharField()
    score = serializers.IntegerField()
    comments = CommentSerializer(many=True)
