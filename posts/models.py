# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import Student, UserProfile, Classroom

class Post(models.Model):
    author = models.ForeignKey(Student, related_name='posts')
    classroom = models.ForeignKey(Classroom, related_name='posts')
    title = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    score = models.IntegerField(default=0)

class Comments(models.Model):
    author = models.ForeignKey(UserProfile, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField(default='')
    score = models.IntegerField(default=0)

