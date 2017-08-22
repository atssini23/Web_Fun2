from django.conf.urls import url
from . import views
app_name = 'review'
urlpatterns = [
    url(r'^books$', views.home, name='home'),
    url(r'^books/add$', views.addbook, name='addbook'),
    url(r'^books/(?P<bookid>\d+)$', views.thisbook, name='thisbook'),
    url(r'^users/(?P<userid>\d+)$', views.thisuser, name='thisuser'),
    url(r'^books/addbooknow$', views.addbooknow, name='add_book_now'),
    url(r'^books/addreview$', views.addreview, name='addreview'),
    url(r'^books/deletereview/(?P<reviewid>\d+)$', views.deletereview,
        name='deletereview'),
]