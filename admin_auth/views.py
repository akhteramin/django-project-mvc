# from django.http import Http404
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import requests
import json
from .services import SERVICE_URL,HEADERS

class IndexView(generic.ListView):
    template_name = 'admin_auth/index.html'


def login(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    loginID = password = ''
    if 'token' in request.session:
        return render(request,'admin_auth/home.html')
    if request.POST:
        loginID = request.POST['loginID']
        password = request.POST['password']
        print(loginID)
        print(password)

        # if 'token' not in request.session:
        if 'token' in request.session:
            return render(request, 'admin_auth/home.html', {
                'login_token':
                    {
                        'token': request.session['token']
                    }
            })
        else:
            post_data = {'loginID': loginID, 'password': password, 'appID': 2, 'deviceID': 'postman'};
            response = requests.post(SERVICE_URL + 'login/', headers=HEADERS, data=json.dumps(post_data))
            print(response.text)
            # if response:
            try:
                token = response.json()
            except Exception as e:
                print(e)
                # Redisplay the question voting form.
                msg = "Wrong Credentials"
                # return HttpResponseRedirect(reverse('admin_auth:login', args=(msg,)))
                return render(request, 'admin_auth/login.html', {"error": "wrong credential"})

            print(token)
            request.session['token'] = token['token']
            request.session['loginID'] = request.POST['loginID']


            return HttpResponseRedirect(reverse('admin_auth:home'))

            # return render(request, 'admin_auth/home.html', {
            #     'login_token': token
            # })
            # else:
            #     return HttpResponseRedirect(reverse('admin_auth:login'))

            # return HttpResponseRedirect(reverse('admin_auth:login'))
    return render(request, 'admin_auth/login.html')

def home( request ):
    if 'token' in request.session:
        return render(request,'admin_auth/home.html')
    else:
        return render(request, 'admin_auth/login.html')



def logout(request):
    del request.session['token']
    request.session.modified = True
    return render(request,'admin_auth/login.html')



def create_user(request):
    if 'token' in request.session:
        param_data = "?limit=100&offset=0"
        response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
        applications=response_app_data.json()
        print(response_app_data.content)
        if request.POST:
            print(request.POST['loginID'])
            print(request.POST['password'])
            print(request.POST['appID'])
            post_data = {'loginID': request.POST['loginID'], 'password': request.POST['password'], 'appID': request.POST['appID'], 'deviceID': 'postman'};

            response_data = requests.post(SERVICE_URL + 'create/', headers=HEADERS, data=json.dumps(post_data))
            print(response_data.status_code)


            if response_data.status_code==201:
                return render(request, 'admin_auth/create_user.html', {"message": "User has been created","applications": applications['results']})
            else:
                return render(request, 'admin_auth/create_user.html', {"message": response_data.text,"applications": applications['results']})


        return render(request, 'admin_auth/create_user.html',{"applications": applications['results']})
    else:
        return render(request, 'admin_auth/login.html')


def create_service(request):
    if 'token' in request.session:
        param_data = "?limit=100&offset=0"
        response_app_data = requests.get(SERVICE_URL + 'app/' + param_data, headers=HEADERS)
        applications = response_app_data.json()
        print(response_app_data.content)
        if request.POST:
            print(request.POST['appID'])
            print(request.POST['serviceID'])
            print(request.POST['description'])
            print(request.POST['serviceCategory'])


            post_data = {'appID': request.POST['appID'], 'serviceID': request.POST['serviceID'],
                         'description': request.POST['description'], 'category':request.POST['serviceCategory']};

            response_data = requests.post(SERVICE_URL + 'service/', headers=HEADERS, data=json.dumps(post_data))
            print(response_data.status_code)
            if response_data.status_code==201:
                return render(request, 'admin_auth/create_service.html', {"message": "Service has been created","applications": applications['results']})
            else:
                return render(request, 'admin_auth/create_service.html', {"message": response_data.text,"applications": applications['results']})

        return render(request, 'admin_auth/create_service.html',{"applications": applications['results']})
    else:
        return render(request, 'admin_auth/login.html')


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
                return render(request, 'admin_auth/create_group.html', {"message": "Group has been created","applications": applications['results']})
            else:
                return render(request, 'admin_auth/create_group.html', {"message": response_data.text,"applications": applications['results']})

        return render(request, 'admin_auth/create_group.html',{"applications": applications['results']})
    else:
        return render(request, 'admin_auth/login.html', )

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
                return render(request, 'admin_auth/create_app.html', {"message": "Application has been created"})
            else:
                return render(request, 'admin_auth/create_app.html', {"message": response_data.text})
        return render(request, 'admin_auth/create_app.html')
    else:
        return render(request, 'admin_auth/login.html', )

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
                return render(request, 'admin_auth/edit_app.html', {"message": "Application has been updated","app_details":app_details})
            else:
                return render(request, 'admin_auth/edit_app.html', {"message": response_data.text,"app_details":app_details})


        elif appID!='':
            print(appID)
            response_data = requests.get(SERVICE_URL + 'app/' + appID + "/",
                                           headers=HEADERS)
            app_details=response_data.json()
            return render(request, 'admin_auth/edit_app.html', {"app_details": app_details})
    else:
        return render(request, 'admin_auth/login.html', )

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
                return render(request, 'admin_auth/edit_group.html',
                              {"message": "Group has been updated","group_details":group_details,"applications":applications['results']})
            else:
                return render(request, 'admin_auth/edit_group.html', {"message": response_data.text,"group_details":group_details,"applications":applications['results']})


        elif groupId!='':
            print(groupId)
            response_data = requests.get(SERVICE_URL + 'group/' + groupId + "/",
                                           headers=HEADERS)
            group_details=response_data.json()
            return render(request, 'admin_auth/edit_group.html', {"group_details": group_details,"applications":applications['results']})
    else:
        return render(request, 'admin_auth/login.html', )

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
                return render(request, 'admin_auth/edit_service.html',
                              {"message": "Service has been updated","service_details":service_details,"applications":applications['results']})
            else:
                return render(request, 'admin_auth/edit_service.html', {"message": response_data.text,"service_details":service_details,"applications":applications['results']})


        elif serviceId!='':
            print(serviceId)
            response_data = requests.get(SERVICE_URL + 'service/' + serviceId + "/",
                                           headers=HEADERS)
            print(response_data.content)
            service_details=response_data.json()
            return render(request, 'admin_auth/edit_service.html', {"service_details": service_details,"applications":applications['results']})
    else:
        return render(request, 'admin_auth/login.html', )

def list_user(request):

    if 'token' in request.session:
        searchParam={}
        if 'next_url' in request.POST:
            print("next login id")
            print(request.POST['next_login_id'])
            response_data = requests.get(request.POST['next_url'], headers=HEADERS)
            userList = response_data.json()
            print(response_data.content)
        elif 'prev_url' in request.POST:
            response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
            userList = response_data.json()
            print(response_data.content)
        elif 'login_id' in request.POST and 'app_id' in request.POST:
            paramData=request.POST['login_id']+"/"+request.POST['app_id']+"?limit=5&offset=0"
            searchParam={'login_id':request.POST['login_id'],'app_id':request.POST['app_id']}
            response_data = requests.get(SERVICE_URL + 'user/' + paramData, headers=HEADERS)
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

        return render(request, 'admin_auth/list_user.html',
                      {"users":userList,"applications":appList['results'],'searchParam':searchParam})
    else:
        return render(request, 'admin_auth/login.html', )

def list_group(request):
    if 'token' in request.session:
        if 'next_url' in request.POST:
            response_data = requests.get(request.POST['next_url'], headers=HEADERS)
            groupList = response_data.json()
            print(response_data.content)
        elif 'prev_url' in request.POST:
            response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
            groupList = response_data.json()
            print(response_data.content)

        else:
            postData = "?limit=10&offset=0"
            response_data = requests.get(SERVICE_URL + 'group/' + postData, headers=HEADERS)
            print(response_data.content)
            groupList = response_data.json()
            print(response_data.content)

        return render(request, 'admin_auth/list_group.html', {"groups": groupList})
    else:
        return render(request, 'admin_auth/login.html', )

def list_service(request):
    if 'token' in request.session:
        if 'next_url' in request.POST:
            response_data = requests.get(request.POST['next_url'], headers=HEADERS)
            serviceList = response_data.json()
            print(response_data.content)
        elif 'prev_url' in request.POST:
            response_data = requests.get(request.POST['prev_url'], headers=HEADERS)
            serviceList = response_data.json()
            print(response_data.content)

        else:
            postData = "?limit=10&offset=0"
            response_data = requests.get(SERVICE_URL + 'service/' + postData, headers=HEADERS)
            print(response_data.content)
            serviceList = response_data.json()
            print(response_data.content)
        postData = "?limit=100&offset=0"
        response_data = requests.get(SERVICE_URL + 'app/' + postData, headers=HEADERS)
        appList=response_data.json()
        return render(request, 'admin_auth/list_service.html', {"services": serviceList,"applications":appList['results']})
    else:
        return render(request, 'admin_auth/login.html', )


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

        return render(request, 'admin_auth/list_app.html', {"apps": appList})
    else:
        return render(request, 'admin_auth/login.html', )

def assign_user_group(request,userID='',appID=''):

    if 'token' in request.session:
        if request.POST:
            save_user_group(request.POST.getlist('groupID'),userID)
            postData=load_user_group_list(userID, appID)
            return render(request, 'admin_auth/assign_user_group.html',postData)
        else:
            postData=load_user_group_list(userID,appID)
            return render(request, 'admin_auth/assign_user_group.html',postData)

    else:
        return render(request,'admin_auth/login.html')

# only load Data
def load_user_group_list(userID='',appID=''):
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
            return render(request, 'admin_auth/assign_group_service.html',postData)
        else:
            postData=load_group_service_list(groupID,appID)
            return render(request, 'admin_auth/assign_group_service.html',postData)

    else:
        return render(request,'admin_auth/login.html')

# only load Data
def load_group_service_list(groupID='',appID=''):
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
            if service['serviceID'] == group_service['service']['serviceID']:
                serviceList[count]['assigned'] = 1
                break
            else:
                serviceList[count]['assigned'] = 0
        count += 1
    print(serviceList)
    return {'services': serviceList, 'group': group, 'app': app, 'group_service': group_service_list};

# only load Data
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


def change_password(request):
    if request.POST:

        post_data = {'loginID': request.POST['loginID'], 'password': request.POST['password'],'appID':request.POST['appID']}
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