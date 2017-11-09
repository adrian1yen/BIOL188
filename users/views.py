# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from serializers import UserProfileSerializer
from users import models as user_models


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.all().values('id', 'username')

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            user = user_models.UserProfile.objects.get(user=request.user)
        except user_models.UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data.get('username') or not request.data.get('password') or not request.data.get('role'):
            return Response('Username, password, and role required.', status=status.HTTP_400_BAD_REQUEST)
        if user_models.UserProfile.objects.filter(user__username=request.data['username']).count() > 0:
            return Response('Username already taken.', status=status.HTTP_400_BAD_REQUEST)

        user_object = user_models.UserProfile.get_user_object_by_role(role=request.data['role'])
        data = request.data.copy()
        user = User.objects.create(username=data.pop('username'), password=data.pop('password'))
        new_user = user_object.objects.create(user=user, **data)
        serializer = UserProfileSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
