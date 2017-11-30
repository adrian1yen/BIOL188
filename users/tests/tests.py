# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users import keys as user_keys
from users import models as user_models
from users.permissions import IsInClassroom, CanViewUser
from users.tests import factories as user_factories


class UserTests(APITestCase):
    def test_get_object(self):
        teacher = user_factories.TeacherFactory()
        self.assertEqual(teacher.get_user_object(model=True), user_models.Teacher)

        mentor = user_factories.MentorFactory()
        self.assertEqual(mentor.get_user_object(model=True), user_models.Mentor)

        student = user_factories.StudentFactory()
        self.assertEqual(student.get_user_object(model=True), user_models.Student)

    def test_permission_isInClass(self):
        student = user_factories.StudentFactory()
        classroom = user_factories.ClassroomFactory()
        student.classrooms.add(classroom)
        student.save()


        request = mock.Mock()
        request.user = student.user
        request.resolver_match.kwargs.get = mock.Mock(return_value=classroom.id)
        classPermission = IsInClassroom()
        self.assertEqual(True, classPermission.has_permission(request, None))
        request.resolver_match.kwargs.get = mock.Mock(return_value=classroom.id + 1)
        self.assertEqual(False, classPermission.has_permission(request, None))
        request.resolver_match.kwargs.get = mock.Mock(return_value=None)
        self.assertRaises(Exception('IsInClassroom permission must be used with a url that contains "classroom_id"'))

    def test_permission_CanViewUser(self):
        request = mock.Mock()
        request.META.get = mock.Mock(return_value=reverse('me'))
        userPermission = CanViewUser()
        self.assertEqual(True, userPermission.has_permission(request, None))
        request.META.get = mock.Mock(return_value='super good testing')
        student1 = user_factories.StudentFactory()
        student2 = user_factories.StudentFactory()
        student3 = user_factories.StudentFactory()
        classroom = user_factories.ClassroomFactory()
        student1.classrooms.add(classroom)
        student2.classrooms.add(classroom)
        student1.save()
        student2.save()
        request.user = student1.user
        request.resolver_match.kwargs.get = mock.Mock(return_value=student2.id)
        self.assertEqual(True, userPermission.has_permission(request, None))
        request.resolver_match.kwargs.get = mock.Mock(return_value=student3.id)
        self.assertEqual(False, userPermission.has_permission(request, None))
        request.resolver_match.kwargs.get = mock.Mock(return_value=None)
        self.assertRaises(Exception('CanViewUser permission must be used with a url that contains "user_id"'))

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

    def test_add_class(self):
        classroom = user_factories.ClassroomFactory(code='1234')
        student = user_factories.StudentFactory()
        url = reverse('add-class', kwargs={'user_id': student.id})
        self.client.force_authenticate(user=student.user)

        # Test successful add class
        with mock.patch('users.models.Student.save') as mock_save:
            data = {
                'code': classroom.code
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_save.assert_called_once()

        # Test wrong code
        with mock.patch('users.models.Student.save') as mock_save:
            data = {
                'code': '1234'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data, 'Class with code 1234 was not found.')
            mock_save.assert_not_called()

        # Test teacher adding class
        with mock.patch('users.models.Student.save') as mock_save:
            teacher = user_factories.TeacherFactory()
            url = reverse('add-class', kwargs={'user_id': teacher.id})
            self.client.force_authenticate(user=teacher.user)
            data = {
                'code': classroom.code
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data, 'Teachers cannot add classes. They can only create them.')
            mock_save.assert_not_called()

class ClassroomTest(APITestCase):
   def test_create_classroom(self):
        teacher = user_factories.TeacherFactory()
        url = reverse('classroom-list')

        # Testing successful create
        self.client.force_authenticate(user=teacher.user)
        data = {
           'name': 'namename',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

        # Testing student creating class
        student = user_factories.StudentFactory()
        self.client.force_authenticate(user=student.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Must be a teacher to create a class.')

        # Testing bad data
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Name is required.')
