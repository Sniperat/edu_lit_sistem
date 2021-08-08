from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_message
from .functions import user_func


@csrf_exempt
def event(request):
    print(request)
    json_list = json.loads(request.body)
    print(json_list)
    chat_id = json_list['message']['chat']['id']
    msg_text = json_list['message']['text']
    print(msg_text)
    user = user_func(json_list)
    if msg_text == '/start':
        send_message("To'liq ismingizni kiriting", chat_id)
        user.state = 0
        user.save()
        return HttpResponse()



    if user.state == 0:
        user.fullName = msg_text
        send_message("Telefon raqamingizni yozing", chat_id)
        user.state = 1
        user.save()
        return HttpResponse()

    if user.state == 1:
        user.phone = msg_text
        user.state = 7
        user.save()
        send_message("Ro'yxatdan o'tdingiz", chat_id)
        return HttpResponse()

    return HttpResponse()
    # return JsonResponse({'status': 'true', "message": 'worked'})
