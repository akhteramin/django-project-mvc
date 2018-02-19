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
    template_name = 'admin-auth/index.html'

def login(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    print(SERVICE_URL + 'login/')
    loginID = password = ''
    if 'token' in request.session:
        responsePermission = requests.get(SERVICE_URL + 'permissions/', headers=HEADERS)
        print("response permission::")
        print(responsePermission.text)
        request.session['permissionList'] = responsePermission.json()

        paramData = "?login_id=" + request.session['loginID'] + "&account_status=True&app_id=&limit=10&offset=0"
        response_data = requests.get(SERVICE_URL + 'user/get/' + paramData, headers=HEADERS)
        appList = response_data.json()
        request.session['appList'] = appList['results']

        return render(request,'admin-auth/home.html')
    if request.POST:
        loginID = request.POST['loginID']
        password = request.POST['password']
        device_id = request.user_agent.browser.family+"_"+request.user_agent.browser.version_string+"_"+request.user_agent.os.family+"_"+ request.user_agent.device.family+"_"+str(uuid.uuid4())
        print(device_id)
        print(loginID)
        print(password)

        # if 'token' not in request.session:
        if 'token' in request.session:
            return render(request, 'admin-auth/home.html', {
                'login_token':
                    {
                        'token': request.session['token']
                    }
            })
        else:
            post_data = {'loginID': loginID, 'password': password, 'appID': 2, 'deviceID': device_id};
            print(SERVICE_URL + 'login/')
            response = requests.post(SERVICE_URL + 'login/', headers=HEADERS, data=json.dumps(post_data))
            print(response.text)
            # if response:
            try:
                token = response.json()
            except Exception as e:
                print(e)
                # Redisplay the question voting form.
                msg = "Wrong Credentials"
                # return HttpResponseRedirect(reverse('admin-auth:login', args=(msg,)))
                return render(request, 'admin-auth/login.html', {"error": msg})

            print(token)
            request.session['token'] = token['token']
            request.session['loginID'] = loginID
            HEADERS['token'] = token['token']
            responsePermission = requests.get(SERVICE_URL + 'permissions/', headers=HEADERS)
            print(responsePermission.text)
            request.session['permissionList']=responsePermission.json()

            paramData = "?login_id=" + request.session['loginID'] + "&account_status=True&app_id=&limit=10&offset=0"
            response_data = requests.get(SERVICE_URL + 'user/get/' + paramData, headers=HEADERS)
            appList = response_data.json()
            request.session['appList'] = appList['results']

            print(HEADERS)
            return HttpResponseRedirect(reverse('home'))

    if request.GET.get("appID"):
        return render(request, 'admin-auth/accounts.html', {"appID": request.GET.get("appID")})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def accounts(request):
    # print(request.GET.get('loginID'))
    # print(request.GET.get('appID'))
    # print(request.GET.get('token'))'
    print("here it is")

    if request.GET.get('appID'):
        if request.GET.get('appID') in request.session and request.GET.get('appID') is '6':
            print("appIDDDDD::", request.session[request.GET.get('appID')])
            return HttpResponseRedirect(DEV_URLS['member_service'] + '?token='+request.session[request.GET.get('appID')] + '&loginID=' +request.session['loginID'])
        elif request.GET.get('appID') in request.session and request.GET.get('appID') is '2':
            print("appIDDDDD::", request.session[request.GET.get('appID')])
            return HttpResponseRedirect(DEV_URLS['auth'])
        elif request.GET.get('appID') in request.session and request.GET.get('appID') is '3':
            print("appIDDDDD::", request.session[request.GET.get('appID')])
            return HttpResponseRedirect(DEV_URLS['crm'] + '?token='+request.session[request.GET.get('appID')] + '&loginID=' +request.session['loginID'])
        else:
            print("not appIDDDDD::")
            return render(request, 'admin-auth/accounts.html', {"appID": request.GET.get('appID')})
    if request.POST:
        print("post")
        if request.POST['appID'] in request.session:
            if request.POST['appID'] is '6':
                print("in post appIDDDDD::", request.session[request.POST['appID']])
                return HttpResponseRedirect(DEV_URLS['member_service'] + '?token='+request.session[request.POST['appID']] + '&loginID=' +request.session['loginID'])
            elif request.POST['appID'] is '3':
                print("in post appIDDDDD::", request.session[request.POST['appID']])
                return HttpResponseRedirect(
                    DEV_URLS['crm'] + '?token=' + request.session[request.POST['appID']] + '&loginID=' +
                    request.session['loginID'])
            elif request.POST['appID'] is '2':
                print("in post appIDDDDD::", request.session[request.POST['appID']])
                return HttpResponseRedirect(DEV_URLS['auth'])

        loginID = request.POST['loginID']
        password = request.POST['password']
        device_id = request.user_agent.browser.family + "_" + request.user_agent.browser.version_string + "_" + request.user_agent.os.family + "_" + request.user_agent.device.family+"_"+str(uuid.uuid4())
        print(device_id)
        print(loginID)
        print(password)

        post_data = {'loginID': loginID, 'password': password, 'appID': request.POST['appID'], 'deviceID': device_id};
        print(SERVICE_URL + 'login/')
        response = requests.post(SERVICE_URL + 'login/', headers=HEADERS, data=json.dumps(post_data))
        print(response.text)
        # if response:
        try:
            token = response.json()
        except Exception as e:
            print(e)
            # Redisplay the question voting form.
            msg = "Wrong Credentials"
            # return HttpResponseRedirect(reverse('login', args=(msg,)))
            return render(request, 'admin-auth/accounts.html', {"error": msg,"appID":request.POST['appID']})

        print(token)
        HEADERS['token'] = token['token']
        request.session['token'] = token['token']
        request.session['loginID'] = loginID
        request.session[request.POST['appID']] = token['token']

        paramData = "?login_id="+request.session['loginID']+"&account_status=True&app_id=&limit=100&offset=0"
        response_data = requests.get(SERVICE_URL + 'user/get/' + paramData, headers=HEADERS)
        appList = response_data.json()
        request.session['appList'] = appList['results']
        for app in appList['results']:
            print("appID::"+str(app['appID']))
            if request.POST['appID'] != str(app['appID']):
                paramData = "?appID=" + str(app['appID']) + "&deviceID=" + device_id
                response_data = requests.get(SERVICE_URL + 'token/renew/' + paramData, headers=HEADERS)
                new_token = response_data.json()
                print("request token:::" + new_token['token'])
                request.session[str(app['appID'])] = new_token['token']
                if str(app['appID']) == '2':
                    HEADERS['token'] = new_token['token']
                    request.session['token'] = new_token['token']
                    request.session['loginID'] = loginID

        print("response data:", response_data.content)
        print("app data:", request.POST.get('appID'))

        if request.POST.get('appID') is '6':
            return HttpResponseRedirect(DEV_URLS['member_service']+'?token=' + request.session[request.POST['appID']] + '&loginID=' +request.session['loginID'])
        elif request.POST.get('appID') is '3':
            return HttpResponseRedirect(DEV_URLS['crm'] + '?token=' + request.session[request.POST['appID']] + '&loginID=' +
                request.session['loginID'])
        else:
            return HttpResponseRedirect(DEV_URLS['auth'])

    if request.GET.get("appID"):
        return render(request, 'admin-auth/accounts.html', {"appID": request.GET.get("appID")})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def accountslogout( request ):
    print(HEADERS['token'])
    try:
        # del request.session['token']
        response = requests.get(SERVICE_URL + 'logout/', headers=HEADERS)
        for key in list(request.session.keys()):
            del request.session[key]
        request.session.modified = True
    except Exception as e:
        print(e)
        # Redisplay the question voting form.
        msg = ""
        # return HttpResponseRedirect(reverse('login', args=(msg,)))
        if request.GET.get("appID"):
            return render(request, 'admin-auth/accounts.html', {"appID": request.GET.get("appID")})
        else:
            return render(request, 'admin-auth/accounts.html', {"appID": 2})

    if request.GET.get("appID"):
        return render(request, 'admin-auth/accounts.html', {"appID": request.GET.get("appID")})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def home(request):
    if 'token' in request.session:
        return render(request,'admin-auth/home.html')
    else:
        return render(request, 'admin-auth/accounts.html',{"appID": 2})


def logout(request):
    print(HEADERS['token'])
    # del request.session['token']
    # request.session.modified = True
    # response = requests.get(SERVICE_URL + 'logout/', headers=HEADERS)

    # return render(request,'admin-auth/login.html')
    try:
        # del request.session['token']
        response = requests.get(SERVICE_URL + 'logout/', headers=HEADERS)
        for key in list(request.session.keys()):
            del request.session[key]
        request.session.modified = True
    except Exception as e:
        print(e)
        # Redisplay the question voting form.
        msg = ""
        # return HttpResponseRedirect(reverse('login', args=(msg,)))
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

    return render(request, 'admin-auth/accounts.html', {"appID": 2})


def create_user(request):
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
                return render(request, 'admin-auth/create_user.html', {"message": "User has been created","applications": applications['results'],"status":response_data.status_code})
            else:
                print(response_data.headers)
                return render(request, 'admin-auth/create_user.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})


        return render(request, 'admin-auth/create_user.html',{"applications": applications['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def create_service(request):
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
                return render(request, 'admin-auth/create_service.html', {"message": "Service has been created","applications": applications['results'],"status":response_data.status_code})
            else:
                return render(request, 'admin-auth/create_service.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})

        return render(request, 'admin-auth/create_service.html',{"applications": applications['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def create_group(request):
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
                return render(request, 'admin-auth/create_group.html', {"message": "Group has been created","applications": applications['results'],"status":response_data.status_code})
            else:
                return render(request, 'admin-auth/create_group.html', {"message": response_data.text,"applications": applications['results'],"status":response_data.status_code})

        return render(request, 'admin-auth/create_group.html',{"applications": applications['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def create_app(request):
    if 'token' in request.session:
        if request.POST:
            print(request.POST['appName'])
            print(request.POST['description'])
            post_data = {'appName': request.POST['appName'],
                         'description': request.POST['description']};

            response_data = requests.post(SERVICE_URL + 'app/', headers=HEADERS, data=json.dumps(post_data))
            print(response_data.status_code)
            if response_data.status_code == 201:
                return render(request, 'admin-auth/create_app.html', {"message": "Application has been created","status":response_data.status_code})
            else:
                return render(request, 'admin-auth/create_app.html', {"message": response_data.text,"status":response_data.status_code})
        return render(request, 'admin-auth/create_app.html')
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def edit_app(request,appID=''):
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
                return render(request, 'admin-auth/edit_app.html', {"message": "Application has been updated","app_details":app_details,"status":response_data.status_code})
            else:
                return render(request, 'admin-auth/edit_app.html', {"message": response_data.text,"app_details":app_details,"status":response_data.status_code})


        elif appID!='':
            print(appID)
            response_data = requests.get(SERVICE_URL + 'app/' + appID + "/",
                                           headers=HEADERS)
            app_details=response_data.json()
            return render(request, 'admin-auth/edit_app.html', {"app_details": app_details})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2} )


def edit_group(request,groupId=''):
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
                return render(request, 'admin-auth/edit_group.html',
                              {"message": "Group has been updated","group_details":group_details,"applications":applications['results'],"status":response_data.status_code})
            else:
                return render(request, 'admin-auth/edit_group.html',
                              {"message": response_data.text,"group_details":group_details,"applications":applications['results'],"status":response_data.status_code})


        elif groupId!='':
            print(groupId)
            response_data = requests.get(SERVICE_URL + 'group/' + groupId + "/",
                                           headers=HEADERS)
            group_details=response_data.json()
            return render(request, 'admin-auth/edit_group.html', {"group_details": group_details,"applications":applications['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def edit_service(request,serviceId=''):
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
                return render(request, 'admin-auth/edit_service.html',
                              {"message": "Service has been updated","service_details":service_details,"applications":applications['results'],"status":response_data.status_code})
            else:
                return render(request, 'admin-auth/edit_service.html', {"message": response_data.text,"service_details":service_details,"applications":applications['results'],"status":response_data.status_code})


        elif serviceId!='':
            print(serviceId)
            response_data = requests.get(SERVICE_URL + 'service/' + serviceId + "/",
                                           headers=HEADERS)
            print(response_data.content)
            service_details=response_data.json()
            return render(request, 'admin-auth/edit_service.html', {"service_details": service_details,"applications":applications['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def edit_user(request,loginID=''):
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
                return render(request, 'admin-auth/edit_user.html', {"message": "User can't be removed from all applications. But you can deactivate user.","applications": applications['results'],"status":'400','user_data': user_data, 'user_apps_data': user_apps_data['results']})

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
                return render(request, 'admin-auth/edit_user.html', {"message": "User has been Updated.","applications": applications['results'],"status":response_user_app_data.status_code,'user_data': user_data, 'user_apps_data': user_apps_data['results']})
            else:
                print(response_user_app_data.headers)
                return render(request, 'admin-auth/edit_user.html', {"message": response_user_app_data.text,"applications": applications['results'],"status":response_user_app_data.status_code,'user_data': user_data, 'user_apps_data': user_apps_data['results']})

        return render(request, 'admin-auth/edit_user.html',{"applications": applications['results'],'user_data': user_data, 'user_apps_data': user_apps_data['results']})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})

def list_user(request):
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

        return render(request, 'admin-auth/list_user.html',
                      {"users":userList,"applications":appList['results'],'searchParam':searchParam})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def list_group(request):
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

        return render(request, 'admin-auth/list_group.html',
                      {"groups":groupList,"applications":appList['results'],'searchParam':searchParam})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def list_service(request):
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
        return render(request, 'admin-auth/list_service.html',
                      {"services": serviceList,"applications":appList['results'],'searchParam':searchParam})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def list_app(request):
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

        return render(request, 'admin-auth/list_app.html', {"apps": appList})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def list_activity(request):

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
        return render(request, 'admin-auth/list_activity.html',
                      {"activities": activityList,"applications":appList['results'],'searchParam':searchParam})
    else:
        return render(request, 'admin-auth/accounts.html', {"appID": 2})


def assign_user_group(request,userID='',appID=''):

    if 'token' in request.session:
        if request.POST:
            save_user_group(request.POST.getlist('groupID'),userID)
            postData=load_user_group_list(userID, appID)
            postData['message']= 'User has been successfully assigned to Group.'
            postData['status']= 201
            return render(request, 'admin-auth/assign_user_group.html',postData)
        else:
            postData=load_user_group_list(userID,appID)
            return render(request, 'admin-auth/assign_user_group.html',postData)

    else:
        return render(request,'admin-auth/accounts.html', {"appID": 2})


# only load Data
def load_user_group_list(userID='', appID=''):
    userData = requests.get(SERVICE_URL + 'user/' + userID, headers=HEADERS)
    user = userData.json()
    print(userData.content)

    appData = requests.get(SERVICE_URL + 'app/' + appID, headers=HEADERS)
    app = appData.json()
    print(appData.content)

    response_group_data = requests.get(SERVICE_URL + 'group/filtered/app/' + str(appID), headers=HEADERS)
    grouptList = response_group_data.json()
    print(response_group_data.content)

    response_user_group_data = requests.get(SERVICE_URL + 'user_group/details/user/' + str(userID),
                                            headers=HEADERS)
    user_group_list = response_user_group_data.json()
    print(response_user_group_data.content)
    count = 0
    for group in grouptList:

        for user_group in user_group_list:
            if group['groupID'] == user_group['group']['groupID']:
                grouptList[count]['assigned'] = 1
                break
            else:
                grouptList[count]['assigned'] = 0
        count += 1
    print(grouptList)
    return {'groups': grouptList, 'user': user, 'app': app, 'user_group': user_group_list};


# only load Data
def save_user_group(groupIDList,userID):
    response_user_group_data = requests.get(SERVICE_URL + 'user_group/details/user/' + str(userID),
                                            headers=HEADERS)
    userGroupList = response_user_group_data.json()
    for selectedGroupID in groupIDList:
        exist=0
        count=0;
        for userGroup in userGroupList:
            if str(userGroup['group']['id']) == str(selectedGroupID):
                exist=1
                userGroupList[count]['change']=1
                break
            count += 1
        if exist==0:
            post_data={'group':selectedGroupID,'user':userID}
            saveUserGroup = requests.post(SERVICE_URL + 'user_group/',
                                                    headers=HEADERS, data=json.dumps(post_data))

    for userGroup in userGroupList:
        if 'change' not in userGroup:
            deleteUserGroup = requests.delete(SERVICE_URL + 'user_group/' + str(userGroup['id']),
                                          headers=HEADERS)

    return


def assign_group_service(request,groupID='',appID=''):

    if 'token' in request.session:
        if request.POST:
            save_group_service(request.POST.getlist('serviceID'),groupID)
            postData=load_group_service_list(groupID, appID)
            postData['message'] = 'Group has been successfully assigned to Service.'
            postData['status'] = 201
            return render(request, 'admin-auth/assign_group_service.html',postData)
        else:
            postData=load_group_service_list(groupID,appID)
            return render(request, 'admin-auth/assign_group_service.html',postData)

    else:
        return render(request,'admin-auth/accounts.html', {"appID": 2})


    # only load Data
def load_group_service_list(groupID='', appID=''):
    groupData = requests.get(SERVICE_URL + 'group/' + groupID, headers=HEADERS)
    group = groupData.json()
    print(groupData.content)

    appData = requests.get(SERVICE_URL + 'app/' + appID, headers=HEADERS)
    app = appData.json()
    print(appData.content)

    response_service_data = requests.get(SERVICE_URL + 'service/filtered/app/' + str(appID), headers=HEADERS)
    serviceList = response_service_data.json()
    print(response_service_data.content)

    response_group_service_data = requests.get(SERVICE_URL + 'acl/details/group/' + str(groupID),
                                               headers=HEADERS)
    group_service_list = response_group_service_data.json()
    print(response_group_service_data.content)
    count = 0
    for service in serviceList:

        for group_service in group_service_list:
            if service['id'] == group_service['service']['id']:
                serviceList[count]['assigned'] = 1
                break
            else:
                serviceList[count]['assigned'] = 0
        count += 1
    print(serviceList)
    return {'services': serviceList, 'group': group, 'app': app, 'group_service': group_service_list};


def save_group_service(serviceIDList,groupID):
    response_group_service_data = requests.get(SERVICE_URL + 'acl/details/group/' + str(groupID),
                                            headers=HEADERS)
    groupServiceList = response_group_service_data.json()
    for selectedServiceID in serviceIDList:
        exist=0
        count=0;
        for groupService in groupServiceList:
            if str(groupService['service']['id']) == str(selectedServiceID):
                exist=1
                groupServiceList[count]['change']=1
                break
            count += 1
        if exist==0:
            post_data={'service':selectedServiceID,'group':groupID}
            saveGroupService = requests.post(SERVICE_URL + 'acl/',
                                                    headers=HEADERS, data=json.dumps(post_data))

    for groupService in groupServiceList:
        if 'change' not in groupService:
            deleteUserGroup = requests.delete(SERVICE_URL + 'acl/' + str(groupService['id']),
                                          headers=HEADERS)
    return


def get_device_id():
    if 'nt' in os.name:
        return subprocess.Popen('dmidecode.exe -s system-uuid'.split())
    else:
        return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())


def change_password(request):
    if request.POST:
        # paramData = "?login_id=" + request.POST['loginID'] + "&app_id=&limit=10&offset=0"
        # response_data = requests.get(SERVICE_URL + 'user/get/' + paramData, headers=HEADERS)
        # appList = response_data.json()
        # print(response_data.content)
        # for app in appList['results']:
        #     print(app['appID'])
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


# def check_service_permission(request,serviceID):
#     for permission in request.session['permissionList']:
#         if permission['serviceID']==serviceID:
#             return True
#     return False
