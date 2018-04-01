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
    template_name = 'createData/index.html'


def create_user(request):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications=response_app_data.json()
            print(response_app_data.content)
            if request.POST:
                print(request.POST.getlist('appID'))
                appList = request.POST.getlist('appID')
                device_id = request.user_agent.browser.family + "_" + request.user_agent.browser.version_string + "_" + request.user_agent.os.family + "_" + request.user_agent.device.family
                for app in appList:
                    post_data = {'loginID': request.POST['loginID'], 'password': request.POST['password'], 'appID': app, 'deviceID': device_id};
                    response_data = requests.post(SERVICE_URL + 'create/', headers=HEADERS, data=json.dumps(post_data))
                    print(response_data.status_code)


                if response_data.status_code==201:
                    return render(request, 'createData/create_user.html', {"message": "User has been created","applications": applications['results'],"status":response_data.status_code})
                else:
                    print(response_data.headers)
                    return render(request, 'createData/create_user.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})


            return render(request, 'createData/create_user.html',{"applications": applications['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def create_service(request):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications = response_app_data.json()
            print(response_app_data.content)
            if request.POST:
                post_data = {'appID': request.POST['appID'], 'serviceID': request.POST['serviceID'],
                             'description': request.POST['description'], 'category':request.POST['serviceCategory']};

                response_data = requests.post(SERVICE_URL + 'service/', headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)
                if response_data.status_code==201:
                    return render(request, 'createData/create_service.html', {"message": "Service has been created","applications": applications['results'],"status":response_data.status_code})
                else:
                    return render(request, 'createData/create_service.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})

            return render(request, 'createData/create_service.html',{"applications": applications['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def create_group(request):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications = response_app_data.json()
            print(response_app_data.content)
            if request.POST:
                print(request.POST['appID'])
                print(request.POST['groupID'])
                print(request.POST['description'])
                post_data = {'appID': request.POST['appID'], 'groupID': request.POST['groupID'], 'description': request.POST['description']};

                response_data = requests.post(SERVICE_URL + 'group/', headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)
                if response_data.status_code==201:
                    return render(request, 'createData/create_group.html', {"message": "Group has been created","applications": applications['results'],"status":response_data.status_code})
                else:
                    return render(request, 'createData/create_group.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})

            return render(request, 'createData/create_group.html',{"applications": applications['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def create_app(request):
    try:
        if 'token' in request.session:
            if request.POST:
                print(request.POST['appName'])
                print(request.POST['description'])
                post_data = {'appName': request.POST['appName'],
                             'description': request.POST['description']};

                response_data = requests.post(SERVICE_URL + 'app/', headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)
                if response_data.status_code == 201:
                    return render(request, 'createData/create_app.html', {"message": "Application has been created","status":response_data.status_code})
                else:
                    return render(request, 'createData/create_app.html', {"message": response_data.text,"status":response_data.status_code})
            return render(request, 'createData/create_app.html')
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})