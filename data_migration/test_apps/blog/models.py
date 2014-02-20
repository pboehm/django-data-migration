# -*- coding: utf-8 -*-

from django.db import models

class Author(models.Model):
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)

class Comment(models.Model):
    message = models.TextField()
    author = models.ForeignKey(Author, null=True)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(Author)
    comments = models.ManyToManyField(Comment, related_name="post")
