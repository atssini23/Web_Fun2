# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models


# Create your models here.
class UserManager(models.Manager):
    def registervalidate(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['fname'] or len(postData['fname']) < 3:
            results['errors'].append("First Name must be at least 3 characters")
            results['status'] = False
        if not postData['lname'] or len(postData['lname']) < 3:
            results['errors'].append("Last Name must be at least 3 characters")
            results['status'] = False
        if not postData['username'] or len(postData['username']) < 3:
            results['errors'].append("Username must be at least 3 characters")
            results['status'] = False
        if not postData['dob']:
            results['errors'].append("Birthday is required")
            results['status'] = False
        if not postData['userpassword'] or len(postData['userpassword']) < 8:
            results['errors'].append("Password must be at least 8 characters")
            results['status'] = False
        if postData['cpassword'] != postData['userpassword']:
            results['errors'].append("Passwords do not match")
            results['status'] = False

        # dob = datetime.strptime(postData['dob'], '%Y-%m-%d').date()

        # if dob - datetime.strptime(datetime.now().date(), '%Y-%m-%d') < 13:
        #     results['status'] = False
        #     results['errors'].append('Must be 13 or older')

        if results['status'] is False:
            return results
        user = User.objects.filter(username=postData['username'])
        if user:
            results['status'] = False
            results['errors'].append("Registration Failure, have you tried to login?")
        if results['status']:
            userpassword = bcrypt.hashpw(postData['userpassword'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                fname=postData['fname'],
                lname=postData['lname'],
                email=postData['email'],
                dob=postData['dob'],
                username=postData['username'],
                userpassword=userpassword)
            results['user'] = user
        return results

    def loginvalidate(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        user = User.objects.filter(username=postData['username'])
        try:                # need this try loop if the db is empty.
            user[0]
        except IndexError:
            results['status'] = False
            results['errors'].append("Account or password failure.")
            return results
        if user[0]:
            if user[0].userpassword != bcrypt.hashpw(postData['userpassword'].encode(),
                                                     user[0].userpassword.encode()):
                results['status'] = False
                results['errors'].append("Account or password failure.")
            else:
                results['user'] = user[0].id
        else:
            results['status'] = False
        return results


class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=100, unique=True)
    userpassword = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ", " + self.username
    objects = UserManager()
