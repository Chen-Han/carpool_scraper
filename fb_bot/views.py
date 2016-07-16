from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import json
import service
import requests
# Create your views here.
import bot
from  scraper.settings import ACCESS_TOKEN, VERIFY_TOKEN

def reply(user_id, msg):
    messages = []
    if (type(msg) == str or type(msg) == unicode):
        messages.append(msg)
    else: #assume a list of strings
        messages = msg
    for m in messages:
        data = {
            "recipient": {"id": user_id},
            "message": {"text": m}
        }
        print(user_id)
        print(m)
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, data=json.dumps(data), headers={'Content-Type':'Application/json'})
        print(resp.content)


def handle_messenger(request):
    if (request.method=="GET"):
        return handle_secret(request)
    elif(request.method=="POST"):
        return handle_message(request)
    else:
        return HttpResponseNotFound("Not available")

def handle_secret(request):
    params = request.GET
    if(params['hub.verify_token'] == VERIFY_TOKEN):
        return HttpResponse(params['hub.challenge'])
    return HttpResponseNotFound('Not valid verification')


def handle_message(request):
    data = json.loads(request.body)
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = ""
    try:
        message = data['entry'][0]['messaging'][0]['message']['text']
    except KeyError:
        print("warn, no text found")
    bot_response = bot.get_response(message,sender)
    reply(sender, bot_response)
    return HttpResponse('ok')