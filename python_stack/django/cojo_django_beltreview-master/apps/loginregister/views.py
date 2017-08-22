# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import User
# Create your views here.
def index(request):
    # print 'Black Swan in Australian Roses'
    return render(request, 'loginregister/index.html')

def validate(request):
    # print '54th Massachusetts'
    if request.method == 'POST':
        if request.POST['submit'] == 'register':
            userobject = {
                'name': request.POST['reg_name'],
                'alias': request.POST['reg_alias'],
                'email': request.POST['reg_email'],
                'password': request.POST['reg_password'],
                'confirm': request.POST['reg_confirm']
            }
            print userobject
            errors = User.objects.regvalidate(userobject)
            if errors:
                for message in errors:
                    messages.error(request, message, extra_tags='register')
            else:
                newuser = User.objects.create(
                    name=userobject['name'],
                    alias=userobject['alias'],
                    email=userobject['email'].lower(),
                    password=(
                        bcrypt.hashpw(userobject['password'].encode(),
                                      bcrypt.gensalt())
                    )
                )
                request.session['id'] = newuser.id
                return redirect(reverse('review:home'))
        elif request.POST['submit'] == 'login':
            print 'almost there!'
            logobject = {
                'email': request.POST['log_email'],
                'password': request.POST['log_password']
            }
            login = User.objects.logvalidate(logobject)
            if login['errors']:
                print 'aw yeah'
                messages.error(
                    request, 'Login failed; please try again.',
                    extra_tags='login')
            else:
                request.session['id'] = login['id']
                return redirect(reverse('review:home'))
    # for each in get_messages(request):
    #     print each.extra_tags
    #     print each
    return redirect('/')

def logout(request):
    for sessionkey in request.session.keys():
        del request.session[sessionkey]
    return render(request, 'loginregister/logout.html')

def deleteAllTestRecords(request):
    User.objects.all().delete()
    print 'All user records deleted.'
    return redirect('/')
