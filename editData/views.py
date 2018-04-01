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
    template_name = 'editData/index.html'


def edit_app(request,appID=''):
    try:
        if 'token' in request.session:
            if request.POST:
                print(request.POST['appName'])
                print(request.POST['description'])
                post_data = {'appName': request.POST['appName'],
                             'description': request.POST['description']};

                response_data = requests.patch(SERVICE_URL + 'app/'+appID+"/",
                                               headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)

                response_data = requests.get(SERVICE_URL + 'app/' + appID + "/",
                                               headers=HEADERS)
                app_details = response_data.json()

                if response_data.status_code == 200:
                    return render(request, 'editData/edit_app.html', {"message": "Application has been updated","app_details":app_details,"status":response_data.status_code})
                else:
                    return render(request, 'editData/edit_app.html', {"message": response_data.text,"app_details":app_details,"status":response_data.status_code})


            elif appID!='':
                print(appID)
                response_data = requests.get(SERVICE_URL + 'app/' + appID + "/",
                                               headers=HEADERS)
                app_details=response_data.json()
                return render(request, 'editData/edit_app.html', {"app_details": app_details})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2} )
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def edit_group(request,groupId=''):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications = response_app_data.json()
            print(response_app_data.content)
            if request.POST:
                print(request.POST['appID'])
                print(request.POST['description'])
                post_data = {'appID': request.POST['appID'],
                             'groupID':request.POST['groupID'],
                             'description': request.POST['description']};

                response_data = requests.patch(SERVICE_URL + 'group/'+groupId+"/",
                                               headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)

                response_data = requests.get(SERVICE_URL + 'group/' + groupId + "/",
                                               headers=HEADERS)
                group_details = response_data.json()

                if response_data.status_code == 200:
                    return render(request, 'editData/edit_group.html',
                                  {"message": "Group has been updated","group_details":group_details,"applications":applications['results'],"status":response_data.status_code})
                else:
                    return render(request, 'editData/edit_group.html',
                                  {"message": response_data.text,"group_details":group_details,"applications":applications['results'],"status":response_data.status_code})


            elif groupId!='':
                print(groupId)
                response_data = requests.get(SERVICE_URL + 'group/' + groupId + "/",
                                               headers=HEADERS)
                group_details=response_data.json()
                return render(request, 'editData/edit_group.html', {"group_details": group_details,"applications":applications['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def edit_service(request,serviceId=''):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications = response_app_data.json()
            print(response_app_data.content)
            if request.POST:
                print(request.POST['appID'])
                print(request.POST['description'])
                post_data = {'appID': request.POST['appID'],
                             'serviceID':request.POST['serviceID'],
                             'category':request.POST['serviceCategory'],
                             'description': request.POST['description']};

                response_data = requests.patch(SERVICE_URL + 'service/'+serviceId+"/",
                                               headers=HEADERS, data=json.dumps(post_data))
                print(response_data.status_code)

                response_data = requests.get(SERVICE_URL + 'service/' + serviceId + "/",
                                               headers=HEADERS)
                service_details = response_data.json()

                if response_data.status_code == 200:
                    return render(request, 'editData/edit_service.html',
                                  {"message": "Service has been updated","service_details":service_details,"applications":applications['results'],"status":response_data.status_code})
                else:
                    return render(request, 'editData/edit_service.html', {"message": response_data.text,"service_details":service_details,"applications":applications['results'],"status":response_data.status_code})


            elif serviceId!='':
                print(serviceId)
                response_data = requests.get(SERVICE_URL + 'service/' + serviceId + "/",
                                               headers=HEADERS)
                print(response_data.content)
                service_details=response_data.json()
                return render(request, 'editData/edit_service.html', {"service_details": service_details,"applications":applications['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def edit_user(request,loginID=''):
    try:
        if 'token' in request.session:
            param_data = "?limit=100&offset=0"
            response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
            applications=response_app_data.json()
            print(response_app_data.content)

            response_user_data = requests.get(SERVICE_URL + 'user/' + loginID +'/', headers=HEADERS)
            user_data = response_user_data.json()
            print(response_user_data.content)
            print(user_data['loginID'])

            param_user_app_data = '?login_id=' + user_data['loginID'] + '&account_status=True&app_id=&limit=100&offset=0'
            response_user_app_data = requests.get(SERVICE_URL + 'user/get/' + param_user_app_data, headers=HEADERS)
            user_apps_data = response_user_app_data.json()
            print("user getting data::")
            print(response_user_app_data.content)

            for application in applications['results']:
                application['exist']= False
                for user_apps in user_apps_data['results']:
                    if user_apps['appID'] == application['id']:
                        application['exist'] = True
            print(applications['results'])
            if request.POST:
                print(request.POST.getlist('appID'))
                user_app_list={}
                try:
                    for new_app in request.POST.getlist('appID'):
                        user_app_list['appID']= int(new_app)
                        user_app_list['exist']= False
                        for existing_app in user_apps_data['results']:
                            if 'exist' not in existing_app:
                                existing_app['exist'] = False
                            if user_app_list['appID'] == existing_app['appID']:
                                user_app_list['exist'] = True
                                existing_app['exist'] = True
                                print("user apps apps")
                                print(user_apps_data['results'])
                        print("user apps apps")
                        print(user_apps_data['results'])
                        if user_app_list['exist'] == False:
                            print(user_app_list['appID'])
                            print(user_app_list['exist'])
                            device_id = request.user_agent.browser.family + "_" + request.user_agent.browser.version_string + "_" + request.user_agent.os.family + "_" + request.user_agent.device.family
                            post_data = {'loginID': user_data['loginID'], 'appID': user_app_list['appID'], 'deviceID': device_id};
                            response_data = requests.post(SERVICE_URL + 'update/', headers=HEADERS, data=json.dumps(post_data))
                            print(response_data.status_code)

                    print("out of for loop::")
                    print(user_apps_data['results'])
                    for user_apps in user_apps_data['results']:
                        print(user_apps)
                        if user_apps['exist'] == False:
                            response_delete_user_data = requests.delete(SERVICE_URL + 'user/' + str(user_apps['id']) + '/', headers=HEADERS)
                            print('delete')
                            print(response_delete_user_data.status_code)
                except Exception as e:
                    return render(request, 'editData/edit_user.html', {"message": "User can't be removed from all applications. But you can deactivate user.","applications": applications['results'],"status":'400','user_data': user_data, 'user_apps_data': user_apps_data['results']})

                param_data = "?limit=100&offset=0"
                response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
                applications = response_app_data.json()
                print(response_app_data.content)

                response_user_data = requests.get(SERVICE_URL + 'user/' + loginID + '/', headers=HEADERS)
                user_data = response_user_data.json()
                print(response_user_data.content)
                print(user_data['loginID'])

                param_user_app_data = '?login_id=' + user_data['loginID'] + '&account_status=True&app_id=&limit=100&offset=0'
                response_user_app_data = requests.get(SERVICE_URL + 'user/get/' + param_user_app_data, headers=HEADERS)
                user_apps_data = response_user_app_data.json()
                print(response_user_app_data.status_code)

                for application in applications['results']:
                    application['exist'] = False
                    for user_apps in user_apps_data['results']:
                        if user_apps['appID'] == application['id']:
                            application['exist'] = True
                print(applications['results'])

                if response_user_app_data.status_code==200:
                    return render(request, 'editData/edit_user.html', {"message": "User has been Updated.","applications": applications['results'],"status":response_user_app_data.status_code,'user_data': user_data, 'user_apps_data': user_apps_data['results']})
                else:
                    print(response_user_app_data.headers)
                    return render(request, 'editData/edit_user.html', {"message": response_user_app_data.text,"applications": applications['results'],"status":response_user_app_data.status_code,'user_data': user_data, 'user_apps_data': user_apps_data['results']})

            return render(request, 'editData/edit_user.html',{"applications": applications['results'],'user_data': user_data, 'user_apps_data': user_apps_data['results']})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})
    except Exception as e:
        print(e)
        return render(request, 'admin-auth/accounts.html', {"appID": 2})