from django.conf.urls import url

from . import views

app_name = 'createData'
urlpatterns = [

    url(r'^create/user/$', views.create_user, name='create_user'),
    url(r'^create/group/$', views.create_group, name='create_group'),
    url(r'^create/service/$', views.create_service, name='create_service'),
    url(r'^create/app/$', views.create_app, name='create_app'),

]
