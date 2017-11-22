# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from users import keys

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=15, choices=keys.USER_ROLES, default=keys.STUDENT)

    def get_user_object(self, model=False):
        user_object = self.get_user_model_by_role(self.role)
        if model:
            return user_object
        return user_object.objects.get(id=self.id)

    @staticmethod
    def get_user_model_by_role(role):
        if role == keys.TEACHER:
            return Teacher
        elif role == keys.MENTOR:
            return Mentor
        else:
            return Student

class Teacher(UserProfile):
    pass

class Classroom(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    teacher = models.ForeignKey(Teacher, blank=False, null=False, related_name='classrooms')

class Mentor(UserProfile):
    classrooms = models.ManyToManyField(Classroom, related_name='mentors')
    students = models.ManyToManyField('Student', related_name='mentors')

class Student(UserProfile):
    classrooms = models.ManyToManyField(Classroom, related_name='students')
