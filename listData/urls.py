from django.conf.urls import url

from . import views

app_name = 'listData'
urlpatterns = [

    url(r'^list/user/$', views.list_user, name='list_user'),
    url(r'^list/group/$', views.list_group, name='list_group'),
    url(r'^list/service/$', views.list_service, name='list_service'),
    url(r'^list/app/$', views.list_app, name='list_app'),
    url(r'^list/activity/$', views.list_activity, name='list_activity'),

    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^deactivate_user/$', views.deactivate_user, name='deactivate_user'),
    url(r'^activate_user/$', views.activate_user, name='activate_user'),

]
