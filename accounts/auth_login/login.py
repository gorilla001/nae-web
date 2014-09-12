#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange:
#      History:
#=============================================================================
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
import requests
import json
from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.models import User
from jaeweb.settings import LOGIN_URL, app_key, app_name, auth_key, auth_url

def auth_login(request):
    print "login start"
    content = {}
    auth_token_id = request.GET['token']
    auth_username = request.GET['username']
    url = "%s%s%s%s%s" % (auth_url, "/api/grouprole/?uid=", auth_username, app_key, app_name)
    headers = {'content-type': 'application/json'}
    auth_result = requests.get(url, headers=headers,)
    auth_data = auth_result.json()
    print auth_data
    # if len(auth_data["groups"]) > 0:
    content["Role"] = auth_data["groups"]
    memberurl = "%s%s%s%s%s" % (auth_url, "api/member/?uid=", auth_username, app_key, app_name)
    headers = {'content-type': 'application/json'}
    member_result = requests.get(memberurl, headers=headers,)
    memberdata = member_result.json()
    user_list = User.objects.get(username=auth_username)
    user_list.backend = 'django.contrib.auth.backends.ModelBackend'
    # login(request,user_list)
    request.session.set_expiry(60 * 60 * 3)
    content.update(csrf(request))
    return HttpResponseRedirect('/home')
    # else:
    #     return render_to_response('default/error.html')
