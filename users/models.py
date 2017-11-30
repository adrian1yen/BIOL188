# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models

from users import keys

class UserProfile(models.Model):
    """
    A class for the base user model. Contains a user field for
    Django's auth user.
    """
    user = models.OneToOneField(User)
    role = models.CharField(max_length=15, choices=keys.USER_ROLES, default=keys.STUDENT)

    def get_user_object(self, model=False):
        """
        Gets the user's object (Teacher, Mentor, Student). If model
        is set to True, returns the model object instead.

        :param model: Boolean, defaults to False. If True, returns
                      model instead of instance
        :return: Model or instance of UserProfile based on role
        """
        user_object = self.get_user_model_by_role(self.role)
        if model:
            return user_object
        return user_object.objects.get(id=self.id)

    @staticmethod
    def get_user_model_by_role(role):
        """
        Gets the model related to role

        :param role: Teacher, Mentor, Student
        :return: model of role
        """
        if role == keys.TEACHER:
            return Teacher
        elif role == keys.MENTOR:
            return Mentor
        else:
            return Student

class Teacher(UserProfile):
    """
    A class for the Teacher model
    """
    pass

class Classroom(models.Model):
    """
    A class for the Classroom model
    """
    name = models.CharField(max_length=50, blank=False, null=False)
    teacher = models.ForeignKey(Teacher, blank=False, null=False, related_name='classrooms')
    code = models.CharField(max_length=50, blank=False, null=False, default='', unique=True)

    def __init__(self, *args, **kwargs):
        code = uuid.uuid4()
        kwargs['code'] = code
        super(Classroom, self).__init__(*args, **kwargs)


class Mentor(UserProfile):
    """
    A class for the Teacher model
    """
    classrooms = models.ManyToManyField(Classroom, related_name='mentors')
    students = models.ManyToManyField('Student', related_name='mentors')

class Student(UserProfile):
    """
    A class for the Teacher model
    """
    classrooms = models.ManyToManyField(Classroom, related_name='students')
