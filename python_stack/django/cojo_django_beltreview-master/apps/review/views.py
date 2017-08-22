# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Author, Book, Review
from ..loginregister.models import User
# Create your views here.
def home(request):
    # print 'Heart of Darkness'
    print User.objects.get(id=request.session['id']).alias
    context = {
        'recent_reviews': Review.objects.three_recent(),
        'alias': User.objects.get(id=request.session['id']).alias,
        'books': Book.objects.all()
    }
    return render(request, 'review/home.html', context)

def addbook(request):
    context = {'authors': Author.objects.all()}
    return render(request, 'review/addbook.html', context)

def thisbook(request, bookid):
    context = {
        'id': request.session['id'],
        'thisbook': Book.objects.get(id=bookid),
        'reviews': Review.objects.all().filter(book__id=bookid),
    }
    return render(request, 'review/book.html', context)

def thisuser(request, userid):
    context = {
        'user': User.objects.get(id=userid),
        'review_count': Review.objects.filter(
            creator__id=userid).count(),
        'user_booklist': Book.objects.filter(
            review__creator__id=userid).distinct,
    }
    return render(request, 'review/user.html', context)

def addbooknow(request):
    if request.method == 'POST':
        if request.POST['newauthor']:
            print 'yup'
            result = Author.objects.check_author(request.POST['newauthor'])
            if result['exists']:
                add_author = False
                author = result['author']
                print 'exists'
            else:
                add_author = True
                print 'will add author'
        else:
            if request.POST['authorlist']:
                result = Author.objects.check_author(request.POST['authorlist'])
                print result
                if result['exists']:
                    add_author = False
                    author = result['author']
                else:
                    print 'was it this error?'
                    messages.error(
                        request, 'Something has gone wrong with ' +
                        'your request; try again!'
                    )
                    return redirect(reverse('review:addbook'))
        book_object = {
            'title': request.POST['title'],
            'content': request.POST['content'],
            'rating': request.POST['rating'],
            'authorlist': request.POST['authorlist'],
            'newauthor': request.POST['newauthor']
        }
        # print book_object['content']
        if not Book.objects.validate_book(book_object):
            print 'problem!'
            messages.error(
                request, 'Something has gone wrong with your request;' +
                ' try again!'
            )
            return redirect(reverse('review:addbook'))
        book_exists = Book.objects.check_for_existing_book(book_object)
        if book_exists:
            print book_exists
            book_id = book_exists.id
            book = book_exists
            creator = User.objects.get(id=request.session['id'])
            Review.objects.create(content=request.POST['content'],
                                  rating=int(request.POST['rating']),
                                  book=book,
                                  creator=creator)
            return redirect(reverse('review:thisbook', kwargs={'bookid': book_id}))
        if add_author:
            # print 'yess now we add'
            author = Author.objects.create(name=request.POST['newauthor'])
        new_book = Book.objects.create(
            title=request.POST['title'],
            author=author
        )
        new_book_id = new_book.id
        creator = User.objects.get(id=request.session['id'])
        Review.objects.create(content=request.POST['content'],
                              rating=int(request.POST['rating']),
                              book=new_book,
                              creator=creator)
        return redirect(reverse('review:thisbook', kwargs={'bookid': new_book_id}))
    return redirect(reverse('review:addbook'))

def addreview(request):
    if request.method == 'POST':
        book_id = request.POST['bookid']
        if Review.objects.validate_review(request.POST['content'],
                                          request.POST['rating']):
            Review.objects.create(content=request.POST['content'],
                                  rating=int(request.POST['rating'],),
                                  book=Book.objects.get(id=request.POST
                                                        ['bookid']),
                                  creator=User.objects.get(id=request.session
                                                           ['id']))
    return redirect(reverse('review:thisbook', kwargs={'bookid': book_id}))

def deletereview(request, reviewid):
    this_review = Review.objects.get(id=reviewid)
    if this_review.creator.id == request.session['id']:
        Review.objects.get(id=reviewid).delete()
    return redirect(reverse('review:thisbook',
                            kwargs={'bookid': this_review.book.id}))
