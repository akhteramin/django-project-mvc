from django.conf.urls import url

from . import views

app_name = 'admin-auth'
urlpatterns = [
    # url(r'^login/$', views.LoginView.as_view,name='login'),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accountslogout/$', views.accountslogout, name='accountslogout'),

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^create/user/$', views.create_user, name='create_user'),
    url(r'^create/group/$', views.create_group, name='create_group'),
    url(r'^create/service/$', views.create_service, name='create_service'),
    url(r'^create/app/$', views.create_app, name='create_app'),

    url(r'^edit/app/(?P<appID>\w+)/$', views.edit_app, name='edit_app'),
    url(r'^edit/group/(?P<groupId>\w+)/$', views.edit_group, name='edit_group'),
    url(r'^edit/service/(?P<serviceId>\w+)/$', views.edit_service, name='edit_service'),

    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^deactivate_user/$', views.deactivate_user, name='deactivate_user'),
    url(r'^activate_user/$', views.activate_user, name='activate_user'),

    url(r'^list/user/$', views.list_user, name='list_user'),
    url(r'^list/group/$', views.list_group, name='list_group'),
    url(r'^list/service/$', views.list_service, name='list_service'),
    url(r'^list/app/$', views.list_app, name='list_app'),
    url(r'^list/activity/$', views.list_activity, name='list_activity'),

    url(r'^assign/user/group/(?P<userID>\w+)/(?P<appID>\w+)/$', views.assign_user_group, name='assign_user_group'),
    url(r'^assign/group/service/(?P<groupID>\w+)/(?P<appID>\w+)/$', views.assign_group_service, name='assign_group_service'),


    url(r'^$', views.login, name='login'),

]
