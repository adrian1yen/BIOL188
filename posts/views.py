# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from posts import models as post_models
from posts.serializers import PostSerializer, CommentSerializer
from users import models as user_models
from users.permissions import IsInClassroom, CanViewUser

from rest_framework import mixins


class UserPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewUser]

    def get_queryset(self):
        return post_models.Post.objects.filter(author_id=self.kwargs['author_id'])

    def list(self, request, user_id, *args, **kwargs):
        self.kwargs['author_id'] = user_id
        return super(UserPostViewSet, self).list(request)

class ClassroomPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = post_models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsInClassroom]
    lookup_url_kwarg = 'post_id'

    def create(self, request, classroom_id, *args, **kwargs):
        try:
            student = user_models.Student.objects.get(user=request.user)
        except user_models.Student.DoesNotExist:
            return Response('Must be a student to create a post.', status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        content = request.data.get('content')

        if not title or not content or not classroom_id:
            return Response('Title, content, and classroom id are required.', status=status.HTTP_400_BAD_REQUEST)

        try:
            post = post_models.Post.objects.create(author=student, title=title, content=content, classroom_id=classroom_id)
        except Exception as e:
            print e
            return Response("Something went wrong.", status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.GenericViewSet):
    queryset = post_models.Comments.objects.all()
    # permission_classes = [permissions.IsAuthenticated, CanViewUser]

    def create(self, request, classroom_id, post_id, *args, **kwargs):
        try:
            user_id = user_models.UserProfile.objects.get(user=request.user).id
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')
        if not content:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment = post_models.Comments.objects.create(author_id=user_id, content=content, post_id=post_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
