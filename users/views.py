# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.db.models import Prefetch

from serializers import UserSerializer, UserProfileSerializer, ClassroomSerializer, SimpleClassroomSerializer
from users import models as user_models
from users import keys as user_keys
from posts import models as post_models
from users.permissions import IsInClassroom, CanViewUser


class UserListViewSet(viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        if not request.data.get('username') or not request.data.get('password') or not request.data.get('role'):
            return Response('Username, password, and role required.', status=status.HTTP_400_BAD_REQUEST)
        if user_models.UserProfile.objects.filter(user__username=request.data['username']).count() > 0:
            return Response('Username already taken.', status=status.HTTP_400_BAD_REQUEST)

        user_object = user_models.UserProfile.get_user_model_by_role(role=request.data['role'])
        data = request.data.copy()
        user = User.objects.create_user(username=data.pop('username'), password=data.pop('password'))
        new_user = user_object.objects.create(user=user, **data)
        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewUser]

    def get_object(self):
        extra_fields = []
        if self.kwargs['role'] == user_keys.STUDENT:
            extra_fields = ['posts']
        user = self.kwargs['user_model'].objects.select_related(
            'user',
        ).prefetch_related(
            'classrooms',
            Prefetch('comments', queryset=post_models.Comments.objects.select_related(
                'post'
            )),
            *extra_fields
        ).get(
            id=self.kwargs['user_id']
        )
        return user

    def retrieve(self, request, user_id, *args, **kwargs):
        self.kwargs['user_id'] = user_id
        try:
            user = user_models.UserProfile.objects.get(id=user_id)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.kwargs['role'] = user.role
        self.kwargs['user_model'] = user.get_user_object(model=True)

        return super(UserDetailViewSet, self).retrieve(request)

    @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Retrieve information about the authenticated user
        """
        try:
            user = user_models.UserProfile.objects.get(user=request.user)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_class(self, request, user_id):
        """
        Add a classroom to the authenticated user. Cannot be used with Teachers
        """
        code = request.data.get('code')
        if not code:
            return Response('Class code is required.', status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_models.UserProfile.objects.get(user=request.user).get_user_object()
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user.role == user_keys.TEACHER:
            return Response('Teachers cannot add classes. They can only create them.', status=status.HTTP_403_FORBIDDEN)

        try:
            classroom = user_models.Classroom.objects.get(code=code)
        except user_models.Classroom.DoesNotExist:
            return Response('Class with code {} was not found.'.format(code), status=status.HTTP_404_NOT_FOUND)

        if classroom.id in user.classrooms.values_list('id', flat=True):
            return Response('Class is already added.', status=status.HTTP_400_BAD_REQUEST)
        user.classrooms.add(classroom)
        user.save()
        serializer = SimpleClassroomSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClassroomListViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        name = request.data.get('name')
        if not name:
            return Response('Name is required.', status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = user_models.Teacher.objects.get(user=request.user)
            classroom = user_models.Classroom.objects.create(name=name, teacher=teacher)
        except user_models.Teacher.DoesNotExist:
            return Response('Must be a teacher to create a class.', status=status.HTTP_403_FORBIDDEN)
        except:
            return Response('Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = SimpleClassroomSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClassroomDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = user_models.Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated, IsInClassroom]
    lookup_url_kwarg = 'classroom_id'
