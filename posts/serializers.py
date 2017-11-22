from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    score = serializers.IntegerField()

class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(source='user.username')

class ClassroomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class PostSerializer(serializers.Serializer):
    classroom = ClassroomSerializer()
    author = AuthorSerializer()
    content = serializers.CharField()
    score = serializers.IntegerField()
