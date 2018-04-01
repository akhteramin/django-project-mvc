from django.conf.urls import url

from . import views

app_name = 'editData'
urlpatterns = [

    url(r'^edit/app/(?P<appID>\w+)/$', views.edit_app, name='edit_app'),
    url(r'^edit/user/(?P<loginID>\w+)/$', views.edit_user, name='edit_user'),
    url(r'^edit/group/(?P<groupId>\w+)/$', views.edit_group, name='edit_group'),
    url(r'^edit/service/(?P<serviceId>\w+)/$', views.edit_service, name='edit_service'),

]
