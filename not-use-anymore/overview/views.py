from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth.decorators import require_auth
import requests

# Create your views here.
@require_auth
def index(request):
    #return HttpResponse("Hello,World")
    auth_username = request.session.get('realname')

    url='http://localhost:8383/v1/projects'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()

    url='http://localhost:8383/v1/images'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    images_list=rs.json()

    url="http://localhost:8383/v1/containers"
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    containers_list=rs.json()

    projects_total = len(projects_list) 
    images_total = len(images_list)
    containers_total = len(containers_list)
    return render_to_response('overview.html',
            {
                'auth_username':auth_username,
                'projects_total':projects_total,
                'images_total':images_total,
                'containers_total':containers_total,
             }
    )
