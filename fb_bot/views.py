from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import json
import service
import requests
# Create your views here.
import bot

VERIFY_TOKEN = 'secret'
ACCESS_TOKEN = "EAAYYlI8ZAZBWIBAJCTo5rEHzJcWtnRvNF5dBZBRZBa0HwHlV6ttHpAX6Nj77kSyj16olBMiiPfuf129fcQn9tXRKJr6YhvVsc8i7ZBP2aCZBoqegpClOstCa0ZCafQEZC1FW0rZAe4x1uIuXOXArMjzhoh951ZCZCOJWXlZC97unjTqFOQZDZD"

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print(user_id)
    print(msg)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, data=json.dumps(data), headers={'Content-Type':'Application/json'})
    print(resp.content)

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