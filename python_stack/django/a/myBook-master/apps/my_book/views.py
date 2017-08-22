# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Blog, User


# Create your views here.
def index(request):

    if not checkAuth(request):
        return redirect('/')

    user = User.objects.get(id=request.session.get('id'))
    blogs = Blog.objects.all().order_by('-created_at')[:5]
    context = {
        'user': user,
        'blogs': blogs,
    }
    return render(request, 'my_book/index.html', context)


def addBlog(request):
    print 'kjdksjdkjskdjskjskj'
    if not checkAuth(request):
        return redirect('/')

    if request.POST:
        results = Blog.objects.addBlog(request.POST)
        if results:
            messages.info(request, 'Blog Added')
        else:
            for error in results:
                messages.error(request, error)
            return redirect('mybook:addBlog')
        return redirect('mybook:index')

    user = User.objects.get(id=request.session.get('id'))
    context = {
        'user': user,
    }
    return render(request, 'my_book/addBlog.html', context)


def addLike(request):
    if request.POST:
        results = Blog.objects.addLike(request.POST, request.session['id'])
        if results:
            messages.info(request, 'Liked!')
        else:
            for error in results:
                messages.error(request, error)
        return redirect('mybook:index')


def checkAuth(request):  # Force non-authorized user back to login/registration page
    try:
        if not request.session.get('id'):
            messages.error(request, 'NO.')
            return False
        return True
    except:
        messages.error(request, 'NO')
        return False