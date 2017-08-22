# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login.models import User


# Create your models here.
class BlogManager(models.Manager):
    def addBlog(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['title']) < 1 and len(postData['content']) < 1:
            results['errors'].append('All fields must be filled out')
            results['status'] = False

        user = User.objects.get(id=postData['user_id'])
        if results['status']:

            try:
                blog = Blog.objects.create(
                    title=postData['title'],
                    content=postData['content'],
                    user_id=user,
                )
                blog.save()
            except:
                results['errors'].append('Error: Blog not created')

        return results

    def addLike(self, postData, user_id):
        results = {'status': True, 'errors': []}
        try:
            print 'mskjsdkjskdksjksdjksdjksjksdjskjdkjsdkj'
            blog = Blog.objects.get(postData['blog_id'])
            user = User.objects.get(id=user_id)
            like = Blog.likedBlogs.add(user)
            blog.save()
        except:
            results['errors'].append('Error: not liked')

        return results


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)
    user_id = models.ForeignKey('login.User', related_name='blogs')
    likes = models.ManyToManyField('login.User', related_name='likedBlogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()
