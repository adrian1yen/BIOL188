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
    def setUp(self):
        self.student = user_factories.StudentFactory()
        self.classroom_1 = user_factories.ClassroomFactory()
        self.classroom_2 = user_factories.ClassroomFactory()
        self.student.classrooms.add(self.classroom_1.id)
        self.student.classrooms.add(self.classroom_2.id)
        self.student.save()
        self.post1 = post_factories.PostFactory(
            author=self.student,
            classroom=self.classroom_1,
        )
        self.post2 = post_factories.PostFactory(
            author=self.student,
            classroom=self.classroom_2,
        )
        super(PostTests, self).setUp()

    def test_get_users_posts(self):
        url = reverse('user-post-list', kwargs={'user_id': self.student.id})
        # Test getting all user's classroom's posts
        student = user_models.Student.objects.get(id=self.student.id)
        self.client.force_authenticate(user=student.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data.get('count'), 2)

    def test_get_classrooms_post(self):
        url = reverse('classroom-post-detail', kwargs={'classroom_id': self.classroom_1.id, 'post_id': self.post1.id})
        student = user_models.Student.objects.get(id=self.student.id)
        self.client.force_authenticate(user=student.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data.get('id'), self.post1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        student = user_factories.StudentFactory()
        classroom = user_factories.ClassroomFactory()
        student.classrooms.add(classroom.id)
        student.save()

        url = reverse('classroom-post-list', kwargs={'classroom_id': classroom.id})

        # Test creating post
        data = {
            'title': 'The backstreet boizzzz',
            'content': 'I want it thata way.',
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

        # Test non student making post
        teacher = user_factories.TeacherFactory()
        data = {
            'title': 'Tell me why.',
            'content': "Ain't nothing but a heartbreak? heartache?",
            'classroomId': 2,
        }
        self.client.force_authenticate(user=teacher.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)









