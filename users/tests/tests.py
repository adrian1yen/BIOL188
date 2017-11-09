# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users import keys as user_keys
from users import models as user_models
from users.tests import factories as user_factories

class UserTests(APITestCase):
    def test_get_object(self):
        teacher = user_factories.TeacherFactory()
        self.assertEqual(teacher.get_user_object(), user_models.Teacher)

        mentor = user_factories.MentorFactory()
        self.assertEqual(mentor.get_user_object(), user_models.Mentor)

        student = user_factories.StudentFactory()
        self.assertEqual(student.get_user_object(), user_models.Student)

    def test_create_user(self):
        url = reverse('user-list')

        # Test missing data
        data = {
            'username': 'test',
            'role': user_keys.TEACHER,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Username, password, and role required.')

        # Test teacher creation
        data = {
            'username': 'test',
            'password': 'test',
            'role': user_keys.TEACHER,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_models.Teacher.objects.count(), 1)
        user = user_models.Teacher.objects.get(user__username='test')
        self.assertEqual(response.data, {'id': user.id, 'username': user.user.username, 'role': user.role})

        # Test mentor creation
        data = {
            'username': 'test1',
            'password': 'test',
            'role': user_keys.MENTOR,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_models.Mentor.objects.count(), 1)

        # Test mentor creation
        data = {
            'username': 'test2',
            'password': 'test',
            'role': user_keys.STUDENT,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_models.Student.objects.count(), 1)

        # Test username already taken
        data = {
            'username': 'test',
            'password': 'test',
            'role': user_keys.MENTOR,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Username already taken.')
