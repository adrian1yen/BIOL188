# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.urls import reverse
from django.test import RequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from users import models as user_models
from users.tests import factories as user_factories
from posts.tests import factories as post_factories

class PostTests(APITestCase):

    def test_get_posts(self):
        url = reverse('post-list')

        student = user_factories.StudentFactory()


        # Test getting all user's classroom's posts
        student = user_models.Student.objects.get(id=student.id)
        self.client.force_authenticate(user=student.user)
        classroom_1 = user_factories.ClassroomFactory()
        classroom_2 = user_factories.ClassroomFactory()
        student.classrooms.add(classroom_1.id)
        student.classrooms.add(classroom_2.id)
        student.save()
        post_factories.PostFactory(
            classroom=classroom_1,
        )
        post_factories.PostFactory(
            classroom=classroom_2,
        )


        response = self.client.get(url, format='json')
        self.assertEqual(response.data.get('count'), 2)


        # Test getting specific classroom's posts
        data = {
            'classroom': classroom_1.id
        }

        response = self.client.get(url, data)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data['results'][0].get('classroom').get('id'), classroom_1.id)

    def test_create_post(self):
        url = reverse('post-list')

        student = user_factories.StudentFactory()
        classroom = user_factories.ClassroomFactory()
        student.classrooms.add(classroom.id)
        student.save()

        # Test creating post
        data = {
            'content': 'I want it thata way.',
            'classroom': classroom.id,
        }
        self.client.force_authenticate(user=student.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data.get('classroom').get('id'), classroom.id)
        self.assertEqual(response.data.get('classroom').get('name'), classroom.name)
        self.assertEqual(response.data.get('content'), data.get('content'))
        self.assertEqual(response.data.get('score'), 0)
        self.assertEqual(response.data.get('author').get('id'), student.id)
        self.assertEqual(response.data.get('author').get('username'), student.user.username)


        # Test bad data
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test student posting to classroom they are not in
        data = {
            'content': 'Tell Me why.',
            'classroom': classroom.id + 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


        # Test non student making post
        teacher = user_factories.TeacherFactory()
        data = {
            'content': "Ain't nothing but a mistake.",
            'classroom': 2,
        }
        self.client.force_authenticate(user=teacher.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)









