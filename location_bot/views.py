from __future__ import unicode_literals
import json, vk  
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .buttons import * 
from .bot_config import * 
from django.http import Http404
import random
@csrf_exempt 
def index(request): #return HttpResponse('Ok', content_type="text/plain", status=200)
    if (request.method == "POST"):
        data = json.loads(request.body)# take POST request from auto-generated variable <request.body> in json format
        if (data['secret'] == secret_key):
            if (data['type'] == 'confirmation'):
                return HttpResponse(confirmation_token, content_type="text/plain", status=200) 
            elif(data['type'] == 'message_new'):# if VK server send a message 
                session = vk.Session()
                api = vk.API(session, v=5.107)
                user_id = data['object']['message']['from_id']
                api.messages.send(access_token = token, user_id = str(user_id), message = "Привет! Хочешь устроить встречу с другом? Напиши боту 'Хочу встречу'", random_id=random.randrange(-5000000, 5000000), v=5.107)
                return HttpResponse('ok', content_type="text/plain", status=200)
            #else: 
                #raise Http404
    else:
        return HttpResponse('see you :)')
