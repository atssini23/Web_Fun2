# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from ..loginregister.models import User
class ReviewManager(models.Manager):
    def three_recent(self):
        recent = Review.objects.all().order_by('-created_at')[:3]
        return recent
    def these_reviews(self, bookid):
        these = Review.objects.filter(book__id=bookid)
        return these
    def validate_review(self, content, rating):
        if len(content) > 4 and int(rating) in range(1, 6):
            return True
        else:
            return False
class BookManager(models.Manager):
    def validate_book(self, form_data):
        for each in form_data:
            print form_data[each]
        if (
                len(form_data['title']) > 0 and
                len(form_data['content']) > 4 and
                int(form_data['rating']) in range(1,6)
        ):
            return True
        else:
            return False
    def check_for_existing_book(self, book):
        return (
            Book.objects.filter(title=book['title'])
            .filter(
                Q(author__name=book['authorlist']) |
                Q(author__name=book['newauthor']))).first()
class AuthorManager(models.Manager):
    def check_author(self, authorname):
        print authorname
        if Author.objects.filter(name=authorname):
            result = {
                'exists': True,
                'author': Author.objects.get(name=authorname)
            }
            return result
        else:
            result = {'exists': False}
            return result
class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
class Review(models.Model):
    creator = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    content = models.TextField(max_length=2000)
    rating = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
