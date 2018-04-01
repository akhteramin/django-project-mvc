# from django.http import Http404
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from mysite.settings import SERVICE_URL, HEADERS, DEV_URLS, APP_LIST, APP_URL

import subprocess
import os
import uuid

class IndexView(generic.ListView):
    template_name = 'listData/index.html'

def list_user(request):
    try:
        if 'token' in request.session:
            searchParam={}
            print("headers::")
            print(HEADERS)
            if 'next_url' in request.POST:

                searchParam={'login_id':request.GET['login_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['next_url'], headers=HEADERS)
                userList = response_data.json()
                print(response_data.content)
            elif 'prev_url' in request.POST:
                searchParam={'login_id':request.GET['login_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
                userList = response_data.json()
                print(response_data.content)
            elif 'login_id' in request.POST and 'app_id' in request.POST:

                paramData="?login_id="+request.POST.get('login_id')+"&app_id="+request.POST.get('app_id')+"&limit=10&offset=0"
                searchParam={'login_id':request.POST['login_id'],'app_id':request.POST['app_id']}
                response_data = requests.get(SERVICE_URL + 'user/get/' + paramData, headers=HEADERS)
                userList = response_data.json()
                print(response_data.content)
            else:
                postData="?limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'user/'+postData, headers=HEADERS)
                userList=response_data.json()
                print(response_data.content)

            postData = "?limit=1000&offset=0"
            response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
            appList = response_data.json()

            return render(request, 'listData/list_user.html',
                          {"users":userList,"applications":appList['results'],'searchParam':searchParam})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def list_group(request):
    try:
        if 'token' in request.session:
            print("headers::")
            print(HEADERS)
            searchParam={}
            if 'next_url' in request.POST:
                searchParam={'group_id':request.GET['group_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['next_url'], headers=HEADERS)
                groupList = response_data.json()
                print(response_data.content)
            elif 'prev_url' in request.POST:
                searchParam={'group_id':request.GET['group_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
                groupList = response_data.json()
                print(response_data.content)
            elif 'group_id' in request.POST and 'app_id' in request.POST:
                searchParam={'group_id':request.POST.get('group_id'),'app_id':request.POST.get('app_id')}
                paramData="?group_id="+request.POST.get('group_id')+"&app_id="+request.POST.get('app_id')+"&limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'group/get/' + paramData, headers=HEADERS)
                print(response_data.content)
                groupList = response_data.json()
                print(response_data.content)
            else:
                postData = "?limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'group/' + postData, headers=HEADERS)
                groupList = response_data.json()
                print(response_data.content)

            postData = "?limit=1000&offset=0"
            response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
            appList = response_data.json()

            return render(request, 'listData/list_group.html',
                          {"groups":groupList,"applications":appList['results'],'searchParam':searchParam})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def list_service(request):
    try:
        if 'token' in request.session:
            searchParam = {}
            if 'next_url' in request.POST:
                searchParam={'service_id':request.GET['service_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['next_url'], headers=HEADERS)
                serviceList = response_data.json()
                print(response_data.content)
            elif 'prev_url' in request.POST:
                searchParam={'service_id':request.GET['service_id'],'app_id':request.GET['app_id']}
                response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
                serviceList = response_data.json()
                print(response_data.content)

            elif 'service_id' in request.POST and 'app_id' in request.POST:
                searchParam = {'service_id': request.POST.get('service_id'), 'app_id': request.POST.get('app_id')}
                paramData="?service_id="+request.POST.get('service_id')+"&app_id="+request.POST.get('app_id')+"&limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'service/get/' + paramData, headers=HEADERS)
                print(response_data.content)
                serviceList = response_data.json()
                print(response_data.content)

            else:
                print(request.POST);
                postData = "?limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'service/' + postData, headers=HEADERS)
                serviceList = response_data.json()
                print(response_data.content)
            postData = "?limit=1000&offset=0"
            response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
            appList=response_data.json()
            return render(request, 'listData/list_service.html',
                          {"services": serviceList,"applications":appList['results'],'searchParam':searchParam})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def list_app(request):
    try:
        if 'token' in request.session:
            if 'next_url' in request.POST:
                response_data = requests.get(request.POST['next_url'], headers=HEADERS)
                appList = response_data.json()
                print(response_data.content)
            elif 'prev_url' in request.POST:
                response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
                appList = response_data.json()
                print(response_data.content)

            else:
                postData = "?limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
                print(response_data.content)
                appList = response_data.json()
                print(response_data.content)

            return render(request, 'listData/list_app.html', {"apps": appList})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def list_activity(request):
    try:
        if 'token' in request.session:
            searchParam = {}
            if 'next_url' in request.POST:
                searchParam={'service_name':request.GET['service_id'],'app_id':request.GET['app_id'], 'login_id':request.GET['login_id']}
                response_data = requests.get(request.POST['next_url'], headers=HEADERS)
                activityList = response_data.json()
                print(response_data.content)
            elif 'prev_url' in request.POST:
                searchParam={'service_name':request.GET['service_id'],'app_id':request.GET['app_id'], 'login_id':request.GET['login_id']}
                response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
                activityList = response_data.json()
                print(response_data.content)

            elif 'service_id' in request.POST and 'app_id' in request.POST and 'login_id' in request.POST:
                searchParam = {'service_name': request.POST.get('service_id'), 'app_id': request.POST.get('app_id'), 'login_id':request.POST.get('login_id')}
                paramData="?service_name="+request.POST.get('service_id')+"&app_id="+request.POST.get('app_id')+"&login_id="+request.POST.get('login_id')+"&limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'activity/get/' + paramData, headers=HEADERS)
                print(response_data.content)
                activityList = response_data.json()
                print(response_data.content)

            else:
                print(request.POST);
                postData = "?limit=10&offset=0"
                response_data = requests.get(SERVICE_URL + 'activity/' + postData, headers=HEADERS)
                activityList = response_data.json()
                print(response_data.content)
            postData = "?limit=1000&offset=0"
            response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
            appList=response_data.json()
            return render(request, 'listData/list_activity.html',
                          {"activities": activityList,"applications":appList['results'],'searchParam':searchParam})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def change_password(request):
    if request.POST:
        post_data = {'loginID': request.POST['loginID'], 'password': request.POST['password'],'appID': request.POST['appID']}
        change_password = requests.put(SERVICE_URL + 'password/set/',
                                         headers=HEADERS, data=json.dumps(post_data))
        print(change_password.status_code)
        if change_password.status_code==204:
            return HttpResponse(
                json.dumps({"message":"password has been Updated"}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"message": "password Can not be Updated"}),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def deactivate_user(request):
    if request.POST and 'token' in request.session:
        post_data = {'loginID': request.POST['loginID'], 'appID': request.POST['appID']}
        deactivate_data = requests.put(SERVICE_URL + 'account/deactivate/',
                                       headers=HEADERS, data=json.dumps(post_data))
        print(deactivate_data.status_code)
        print(deactivate_data.content)
        return HttpResponse(
            json.dumps({"message": "User has been deactivated"}),
            content_type="application/json"
        )


def activate_user(request):
    if request.POST and 'token' in request.session:
        post_data = {'loginID': request.POST['loginID'], 'appID': request.POST['appID']}
        deactivate_data = requests.put(SERVICE_URL + 'account/reactivate/',
                                       headers=HEADERS, data=json.dumps(post_data))
        print(deactivate_data.status_code)
        print(deactivate_data.content)
        return HttpResponse(
            json.dumps({"message": "User has been activated"}),
            content_type="application/json"
        )

