from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests
import utils

# Create your views here.

def index(request):
    #image_list=[]
    #result=requests.get('http://localhost:8383/v1/images')
    #result_dict=result.json()
    #for res in result_dict:
    #    _dict={}
    #    _dict['Container_Id']=res['Id'][:12]
    #    _dict['Name']=res['RepoTags'][0]
    #    _dict['VirtualSize']=utils.byte_to_gb(res['VirtualSize'])
    #    _dict['Created']=utils.timestamp_to_local(res['Created'])
    #    _dict['Environ']='develop'
    #    image_list.append(_dict)
    #return render_to_response('images.html',data=image_list)
    return render_to_response('images.html')
