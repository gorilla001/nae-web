from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
import requests
import json
from django.contrib.auth.models import User
from jaeweb.settings import LOGIN_URL, app_key, app_name, auth_key, auth_url
from django.contrib.auth import authenticate, login
import hashlib, time


def auth_login(request):
    auth_username = request.GET.get('username')

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

    if 'errormsg' in auth_data:
	return
    if 'admin' in auth_data['groups']:
        request.session['user_role']='admin'

    url = "%s%s%s%s%s" % (auth_url, "/api/allkey/?",app_key, auth_key, app_name)
    headers = {'content-type': 'application/json'}
    auth_result = requests.get(url, headers=headers,)
    for item in auth_result.json():
        if item['uid'] == auth_username :
            request.session['user_key'] = item['key']
    request.session.set_expiry(6000)

    return HttpResponseRedirect('/')
