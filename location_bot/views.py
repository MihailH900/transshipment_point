from __future__ import unicode_literals
import json, vk  
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .models import VK_sender
from .buttons import * 
from .bot_config import * 
from django.http import Http404
import random

@csrf_exempt 
def index(request):
    if request.method == "POST":
        data = json.loads(request.body)# take POST request from auto-generated variable <request.body> in json format
        if data['secret'] == secret_key:
            if data['type'] == 'confirmation':
                return HttpResponse(confirmation_token, content_type="text/plain", status=200) 
            elif data['type'] == 'message_new':# if VK server send a message
                session = vk.Session()
                api = vk.API(session, v=5.107)
                vk_link =  'https://vk.com/eugenef12'
                vk_friend_link = ''
                keyboards = [0]*3 
                keyboards[0] = { 
                    "one_time": True, 
                    "buttons": [ 
                     [text_button(label='Знаю место и хочу назначить там встречу', color = 'positive')], 
                     [text_button(label='Еще не определился с выбором места', color = 'positive')]
                    ]
                }
                keyboards[1] = { 
                    "one_time": True, 
                    "buttons": [ 
                     [location_button()], 
                    ]
                }
                keyboards[2] = { 
                    "one_time": True, 
                    "buttons": [ 
                     [link_button(link='https://yandex.ru/', label = 'Ссылка на сайт:')], 
                     [text_button(label='Еще не определился с выбором места', color = 'positive')]
                    ]
                }
                for i in range(len(keyboards)):
                    keyboards[i] = json.dumps(keyboards[i], ensure_ascii=False).encode('utf-8')
                    keyboards[i] = str(keyboards[i].decode('utf-8'))
                user_id = data['object']['message']['from_id']
                text = data['object']['message']['text']
                sender = VK_sender()
                sender.user_id = user_id
                sender.count = 0 
                d = VK_sender.objects.all()
                senderLast = 0
                if len(d) != 0:
                    senderLast = d[len(d) - 1]
                if text == "delete":
                    VK_sender.objects.all().delete()

                if len(d) == 0 and text == "Начать":
                    sender.text = text
                    sender.meet_location_x = -1
                    sender.meet_location_y = -1
                    sender.count = 0
                    sender.save()
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Привет! Хочешь устроить встречу с другом? Напиши боту 'Хочу встречу'. Если в какой-то момент тебе не захочется продолжать, напиши команду delete, и вся история сотрётся.", random_id=random.randrange(-5000000, 5000000), v=5.107) 
                elif senderLast == 0 and text != "Начать":
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Хей, напиши 'Начать' для старта. Давай ка ещё раз", random_id=random.randrange(-5000000, 5000000), v=5.107)

                if len(d) == 1 and text == "Хочу встречу":
                    sender.text = text
                    sender.meet_location_x = -1
                    sender.meet_location_y = -1
                    sender.count = 1
                    sender.save()
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Как ты хочешь встретиться?", random_id=random.randrange(-5000000, 5000000), v=5.107, keyboard=keyboards[0])
                elif len(d) == 1 and text != "Хочу встречу":
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Хей, я просил написать 'Хочу встречу'. Давай ка ещё раз", random_id=random.randrange(-5000000, 5000000), v=5.107)

                if senderLast.count == 1 and  text == "Знаю место и хочу назначить там встречу":
                    sender.text = text
                    sender.meet_location_x = -1
                    sender.meet_location_y = -1
                    sender.count = senderLast.count + 1 
                    sender.save() 
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Выбери место встречи:", random_id=random.randrange(-5000000, 5000000), v=5.107, keyboard = keyboards[1])
                elif senderLast.count == 1 and text == "Еще не определился с выбором места":
                    pass
                elif senderLast.count == 1 and text != "Знаю места встречи и хочу назначить там встречу" and text != "Ещё не определился с выбором места":
                    api.messages.send(access_token = token, user_id = str(user_id) , message = "Хей, я просил выбрать одно из двух. Давай ка ещё раз", random_id=random.randrange(-5000000, 5000000), v=5.107, keyboard=keyboards[0])

                if senderLast.count == 2 and text == "":
                    sender.text = chr(18) +  str(data['object']['message']['geo']['coordinates']['latitude']) + ' ' + str(data['object']['message']['geo']['coordinates']['longitude'])
                    sender.meet_location_x = data['object']['message']['geo']['coordinates']['latitude']
                    sender.meet_location_y = data['object']['message']['geo']['coordinates']['longitude']
                    sender.count = senderLast.count + 1 
                    sender.save()
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Отлично! Теперь отправь нам ссылку на своего друга", random_id=random.randrange(-5000000, 5000000), v=5.107)
                elif senderLast.count == 2 and text != "":
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Хей, я же просил отметить себя на карте. Давай ка ещё раз", random_id=random.randrange(-5000000, 5000000), v=5.107, keyboard=keyboards[1])

                if senderLast.count == 3 and text[:15] == vk_link[:15]:
                    vk_friend_link = text[15:]
                    friend_massiv = api.users.get(access_token = token, user_ids = vk_friend_link, v = 5.107)
                    friend_id = friend_massiv[0]['id']
                    api.messages.send(access_token = token, user_id = str(friend_id), message = "Привет! С тобой хочет встретится https://vk.com/" + str(user_id) + "\n Напиши 'Встретится', если готов встретится или напиши 'Отказ от встречи', если отказываешься", random_id = random.randrange(-500000, 500000), v=5.107)
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Приглашение отправлено!", random_id=random.randrange(-5000000, 5000000), v=5.107)
                    sender.text = text
                    sender.meet_location_x = -1
                    sender.meet_location_y = -1
                    sender.count = senderLast.count + 1
                    sender.save()
                elif senderLast.count == 3 and text[:15] != vk_link[:15]:
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Хей, это не ссылка. Давай ка ещё раз, только ссылку", random_id=random.randrange(-5000000, 5000000), v=5.107)

                if senderLast.count == 4 and text == "Встретится":
                    m_x = d[len(d)-2].meet_location_x
                    m_y = d[len(d)-2].meet_location_y
                    api.messages.send(access_token = token, user_id = str(user_id), message = "Ссылка: http://alice.dqpig.ml/cartGenerate/?m_x=" + str(m_x) + '&m_y=' + str(m_y), random_id = random.randrange(-5000000, 5000000), v =5.107)
                    api.messages.send(access_token = token, user_id = d[len(d) - 1].user_id, message = "Ссылка: http://alice.dqpig.ml/cartGenerate/?m_x=" + str(m_x) + '&m_y=' + str(m_y) , random_id = random.randrange(-5000000, 5000000), v=5.107)
                    VK_sender.objects.all().delete()
                elif senderLast.count == 4 and text == "Отказ от встречи":
                    api.messages.send(access_token = token, user_id = d[len(d)-1].user_id, message = "Ваш друг не хочет встречаться сейчас, попробуйте позже", random_id=random.randrange(-5000000, 5000000), v=5.107)
                    Vk_sender.objects.all().delete()
                elif senderLast.count == 4 and text != "Встретится" and text != "Отакз от встречи":
                    api.messages.send(access_token = token, user_id = user_id, message = "Хей, я просил сказать 'Встретится'. Давай ка ещё раз", random_id=random.randrange(-5000000, 5000000), v=5.107)
                return HttpResponse('ok', content_type="text/plain", status=200)
            #else: 
                #raise Http404
    else:
        return HttpResponse('see you :)')


def cartGenerate(request):
    context ={
        "m_x": request.GET.get("m_x"),
        "m_y": request.GET.get("m_y")
    }

    return render(request, "cartGenerate.html", context)
