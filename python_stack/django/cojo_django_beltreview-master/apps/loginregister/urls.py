from django.conf.urls import url
from . import views
app_name = 'loginregister'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validate$', views.validate, name='validate'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^deleteAllTestRecords$', views.deleteAllTestRecords, name='deleteAll')
]