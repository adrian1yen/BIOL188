# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from posts import models as post_models
from posts.serializers import PostSerializer
from users import models as user_models


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return post_models.Post.objects.filter(classroom_id__in=self.kwargs['classroom'])

    def list(self, request, *args, **kwargs):
        if request.query_params.get('classroom') != None:
            self.kwargs['classroom'] = [request.query_params.get('classroom')]
        else:
            try:
                id, role = user_models.UserProfile.objects.values_list('id','role').get(user=request.user)
                user_model = user_models.UserProfile.get_user_model_by_role(role)
                self.kwargs['classroom'] = user_model.objects.filter(id=id).values_list('classrooms__id', flat=True) or []
            except user_models.UserProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return super(PostViewSet, self).list(request)

    def create(self, request, *args, **kwargs):
        try:
            student = user_models.Student.objects.get(user=request.user)
        except user_models.Student.DoesNotExist:
            return Response('Must be a student to create a post.', status=status.HTTP_401_UNAUTHORIZED)

        content = request.data.get('content')
        classroom_id = request.data.get('classroomId')

        if not content or not classroom_id:
            return Response('Content and classroom id required.', status=status.HTTP_400_BAD_REQUEST)
        elif classroom_id not in student.classrooms.values_list('id', flat=True):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = post_models.Post.objects.create(author=student, content=content, classroom_id=classroom_id)
        except Exception as e:
            print e
            return Response("Something went wrong.", status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

