from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self,postData):
        print postData
        results = {'status': True, 'errors':[], 'user':None}
        if not postData['first_name'] or len(postData['first_name'])<=2:
            results['status']= False
            results['errors'].append('First Name must contain more characters')
        if not postData['last_name'] or len(postData['last_name'])<=2:
            results['status']= False
            results['errors'].append('Last Name must contain more characters')
        if not EMAIL_REGEX.match(postData['email']):
            results['status']= False
            results['errors'].append('Not a Valid email')
        if not postData['password'] or len(postData['password'])<8:
            results['status']= False
            results['errors'].append('Not a Valid password')
        if str(postData['password']) != str(postData['confirm_password']):
            results['status']= False
            results['errors'].append('passwords do not match')

        if results['status']:
            new_user = User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = postData['password']
            )
            results['user'] = new_user
        return results

    def login(self, postData):
        results = {'status':True, 'errors':[], 'user':None}
        try:
            results['user']= User.objects.get(email= postData['email'])
        except:
            results['status']= False
            results['errors'].append('no email or password')
            return results

        if str(results['user'].password) == str(postData['password']):
            results['status']= True
        else:
            results['status']= False
            results['errors'].append('no email or password')
        return results

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
