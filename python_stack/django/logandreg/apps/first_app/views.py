from __future__ import unicode_literals

from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from .models import User, UserManager

def index(request):
    all_users = User.objects.all()
    for user in all_users:
        print user.first_name, user.last_name, user.email, user.password
    return render(request, 'first_app/index.html')

def register(request):
    print request.POST
    user_manager = UserManager()
    results = user_manager.register(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
    else:
        messages.success(request, 'Your are now a user. Please login.')
    return redirect('/')

def login(request):
    user_manager = UserManager()
    results = user_manager.login(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        messages.success(request, 'You have successfully logged in!')
    return render(request, 'first_app/success.html')
