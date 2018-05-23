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

    url(r'^assign/user/group/(?P<userID>\w+)/(?P<appID>\w+)/$', views.assign_user_group, name='assign_user_group'),
    url(r'^assign/group/service/(?P<groupID>\w+)/(?P<appID>\w+)/$', views.assign_group_service, name='assign_group_service')
]
