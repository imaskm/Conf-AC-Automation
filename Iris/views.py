# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Master
from .serializers import serialize

import json


def index(request):
    return HttpResponse("Test for EagleEye.")


def home(request):
    posts = Master.objects.all()
    # print "here are the posts\n" + posts
    return render(request, 'home.html', {'posts': posts})


# TODO
def popup(request):
    return render(request, 'help_popup.html')


def ajax_up(request):
    posts = Master.objects.all()
    data = serialize('json', posts)
    data_temp = json.loads(data)
    data = json.dumps(data_temp)

    print data
    return HttpResponse(data, content_type='application/json')

