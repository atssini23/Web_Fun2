# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regvalidate(self, form_data):
        errors = []
        if len(form_data['name']) < 2 or not form_data['name'].isalpha():
            errors.append(
                'Name must include no fewer than two ' +
                'characters and include alphabetic characters only.'
            )
        if len(form_data['alias']) < 2:
            errors.append(
                'Alias must include no few than 2 alphanumeric ' +
                'characters, of which at least one must be a letter.'
            )
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append(
                'Please enter a valid email address.'
            )
        if len(form_data['password']) < 8:
            errors.append('Password must include at least eight characters.')
        if form_data['password'] != form_data['confirm']:
            errors.append('Passwords do not match.')
        return errors
    def logvalidate(self, form_data):
        results = {
            'errors': False,
            'id': None,
        }
        print 'Diamine Ox Blood'
        try:
            founduser = User.objects.get(email=form_data['email'])
            print founduser.password
            print form_data['password']
            if founduser.password == bcrypt.hashpw(
                    form_data['password'].encode(),
                    founduser.password.encode()
            ):
                results['id'] = founduser.id
                print 'Baystate Blue'
                return results
            else:
                results['errors'] = True
            return results
        except:
            print "Noodler's Dark Matter"
            results['errors'] = True
        return results

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
