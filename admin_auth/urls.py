from django.conf.urls import url

from . import views

app_name = 'admin_auth'
urlpatterns = [
    # url(r'^login/$', views.LoginView.as_view,name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^create_service/$', views.create_service, name='create_service'),
    url(r'^create_app/$', views.create_app, name='create_app'),

    url(r'^edit_app/(?P<appID>\w+)/$', views.edit_app, name='edit_app'),
    url(r'^edit_group/(?P<groupId>\w+)/$', views.edit_group, name='edit_group'),
    url(r'^edit_service/(?P<serviceId>\w+)/$', views.edit_service, name='edit_service'),

    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^deactivate_user/$', views.deactivate_user, name='deactivate_user'),
    url(r'^activate_user/$', views.activate_user, name='activate_user'),

    url(r'^list_user/$', views.list_user, name='list_user'),
    url(r'^list_group/$', views.list_group, name='list_group'),
    url(r'^list_service/$', views.list_service, name='list_service'),
    url(r'^list_app/$', views.list_app, name='list_app'),
    url(r'^assign_user_group/(?P<userID>\w+)/(?P<appID>\w+)/$', views.assign_user_group, name='assign_user_group'),
    url(r'^assign_group_service/(?P<groupID>\w+)/(?P<appID>\w+)/$', views.assign_group_service, name='assign_group_service'),


    url(r'^$', views.login, name='login'),

]
