from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^ninja/(?P<color>\w+)$', views.each),
    url(r'^all$', views.all),
    url(r'^$', views.index)
]
