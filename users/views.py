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

from serializers import UserSerializer, UserProfileSerializer
from users import models as user_models
from users import keys as user_keys
from posts import models as post_models


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.all().values('id', 'username')

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

    def retrieve(self, request, userId, *args, **kwargs):
        self.kwargs['user_id'] = userId
        try:
            user = user_models.UserProfile.objects.get(id=userId)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.kwargs['role'] = user.role
        self.kwargs['user_model'] = user.get_user_object(model=True)

        return super(UserViewSet, self).retrieve(request)

    @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            user = user_models.UserProfile.objects.get(user=request.user)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class UserProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserProfileSerializer

    def get_object(self):
        if self.kwargs['role'] == user_keys.TEACHER:
            queryset = self.kwargs['user_model'].values(
                'id',
                'user__username',
                'role',
                'classrooms_id',
                'classrooms__name',
                'comments__id',
            ).get(id=self.kwargs['user_id'])

            print queryset

    def retrieve(self, request, *args, **kwargs):
        try:
            user = user_models.UserProfile.objects.get(user=request.user)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.kwargs['user_id'] = user.id
        self.kwargs['role'] = user.role
        self.kwargs['user_model'] = user.get_user_object(model=True)

        return super(UserProfileViewSet, self).retrieve(request)
