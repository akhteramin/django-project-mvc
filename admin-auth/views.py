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
        try:
            appList = response_data.json()
            request.session['appList'] = appList['results']
        except Exception as e:
            print(e)
        return render(request, 'admin-auth/home.html')
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

            try:
                appList = response_data.json()
                request.session['appList'] = appList['results']
            except Exception as e:
                print(e)

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
        try:
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
        except Exception as e:
            print(e)
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


# def check_service_permission(request,serviceID):
#     for permission in request.session['permissionList']:
#         if permission['serviceID']==serviceID:
#             return True
#     return False
