# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import list_route
from serializers import UserProfileSerializer
from users import models as user_models
from users import keys as user_keys

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
        # if user.role == user_keys.TEACHER:
        #     user = user_models.Teacher.objects.get(user=request.user)
        # elif user.role == user_keys.MENTOR:
        #     user = user_models.Mentor.objects.get(user=request.user)
        # else:
        #     user = user_models.Student.objects.get(user=request.user)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
