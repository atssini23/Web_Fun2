from django.conf.urls import url
from.import views

app_name = 'mybook'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addBlog$', views.addBlog, name='addBlog'),
    url(r'^addLike$', views.addLike, name='addLike'),
]
