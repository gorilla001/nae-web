from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
import requests
import json
from django.contrib.auth.models import User
from jaeweb.settings import LOGIN_URL, app_key, app_name, auth_key, auth_url
from django.contrib.auth import authenticate, login
import hashlib, time
import pprint

# Create your views here.
def auth_login(request):
    auth_username = request.GET['username']
    request.session['is_authed'] = True;
    url = "{}{}{}{}{}{}".format(auth_url,"/api/member/?uid=",auth_username,app_key,auth_key,app_name)
    headers={'Content-Type':'application/json'}
    auth_result = requests.get(url, headers=headers)
    resp_data = auth_result.json()
    if 'success' in resp_data:
        user_id = resp_data['username'] 
        user_name = resp_data['fullname']

        request.session['user_id'] = user_id 
        request.session['user_name'] = user_name 
    url = "%s%s%s%s%s%s" % (auth_url, "/api/grouprole/?uid=", auth_username, app_key, auth_key, app_name)
    headers = {'content-type': 'application/json'}
    auth_result = requests.get(url, headers=headers,)
    auth_data = auth_result.json()

    if 'admin' in auth_data['groups']:
        request.session['user_role']='admin'

    url = "%s%s%s%s%s" % (auth_url, "/api/allkey/?",app_key, auth_key, app_name)
    headers = {'content-type': 'application/json'}
    auth_result = requests.get(url, headers=headers,)
    for item in auth_result.json():
        if item['uid'] == auth_username :
            request.session['user_key'] = item['key']
            print request.session['user_key']
    print url
    print auth_result.json()
    #url= http://auth.jumeird.com/api/allkey/?app_key=1adcdec244fb11e28dbe7cd1c3eeb629&app_name=optool_jumei
    request.session.set_expiry(6000)
    return HttpResponseRedirect('/')
    #if len(auth_data["groups"]) > 0:
    #content["Role"] = auth_data["groups"]
    #memberurl = "%s%s%s%s%s" % (auth_url, "api/member/?uid=", auth_username, app_key, app_name)
    #headers = {'content-type': 'application/json'}
    #member_result = requests.get(memberurl, headers=headers,)
    #memberdata = member_result.json()
    #user_list = User.objects.get(username=auth_username)
    #user_list.backend = 'django.contrib.auth.backends.ModelBackend'
    ## login(request,user_list)
    #session_id = hashlib.sha1(auth_token_id + "481986a634ca11e4ab8c842b2b738d12" + auth_username).hexdigest()
    #user.backend = 'django.contrib.auth.backends.ModelBackend'
    #login(request,user)
    #request.session.set_expiry(60 * 1 )
    #request.session["session_id"] = "asdfasdfasdfadsf89089089sadfasd342340"
    #content.update(csrf(request))
    ## else:
    #     return render_to_response('default/error.html')
