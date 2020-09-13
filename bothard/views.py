from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
from slacker import Slacker
import schedule
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Report
import time



dict={}
@csrf_exempt
def event_check(request):
    global dict
    client=Slacker('token_key')
    json_dict = json.loads(request.body.decode('utf-8'))
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    if 'event' in json_dict:
        event_msg = json_dict['event']
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)
    if event_msg['type'] == 'message':
        user = event_msg['user']
        #To check the message recieved is not of bot himself
        if user!='bot_userid' and user in dict:
            dict[user]+=1
        if user!='bot_userid'' and user not in dict:
            dict[user]=1
        if user!='bot_userid':
            error=False
            try:
                print(Report.objects.values('user'))
                if(Report.objects.get(user__exact=str(user))):
                    pass
            except Exception as e:
                print("re2")
                error=True
            if error==False and Report.objects.get(user__exact=str(user)):
                instance=Report.objects.get(user__exact=str(user))
                print("reached")
                if dict[user]==1:
                    instance.yesterday=event_msg['text']
                if dict[user]==2:
                    instance.today=event_msg['text']
                if dict[user]==3:
                    instance.obstacles=event_msg['text']
                instance.save()
            else:
                report=Report()
                report.user=user
                if dict[user]==1:
                    report.yesterday=event_msg['text']
                if dict[user]==2:
                    report.today=event_msg['text']
                if dict[user]==3:
                    report.obstacles=event_msg['text']
                report.save()

            list_stack(user,dict)
        return HttpResponse(status=200)
    return HttpResponse(status=200)
# Create your views here.

def list_stack(user='user',dict={}):

    slack=Slacker('token_key')

    if user=='user':

        try:
            response=slack.users.list()
            users=response.body['members']
            for user in users:
                if not user['deleted']:
                        id=user['id']
                        slack.chat.post_message('@%s'%id,'What Did you do yesterday!')
                        print("\n")

        except KeyError as ex:
            print("environment Variable {} not set".format(str(ex)))

    else:
        if user in dict and dict[user]==1:
            slack.chat.post_message('@%s'%user,'What are you planning to do today?')
        elif user in dict and dict[user]==2:
            slack.chat.post_message('@%s'%user,'Did you have any Blockers?')
        elif user in dict and dict[user]==3:
            slack.chat.post_message('@%s'%user,'Okay Great! Keep going.')
            return None
        elif user not in dict or dict[user]<3:
            slack.chat.post_message('@%s'%user,'What Did you do yesterday!')


def post_report():
    global dict
    slack=Slacker('token_key')
    try:
        response=slack.users.list()
        users=response.body['members']
        for user in users:
            if not user['deleted']:
                for i in Report.objects.all():
                    if(i.user==user['id']):
                        slack.chat.post_message('#random',"Activities for <@%s> are:"%i.user)
                        slack.chat.post_message('#random',"For yesterday : {}".format(i.yesterday))
                        slack.chat.post_message('#random',"For today : {}".format(i.today))
                        slack.chat.post_message('#random',"Any Obstacles  : {}".format(i.obstacles))
                        dict[i.user]=0
                        i.delete()
        print("\n")

    except KeyError as ex:
        print("environment Variable {} not set".format(str(ex)))

    return None


scheduler = BackgroundScheduler()
#You can change the time in minutes hours or seconds according to your choice

#This function sends asks the report from the users
scheduler.add_job(list_stack,'interval',seconds =60)
#This function will wrap up the report and send the output to the #random channel
scheduler.add_job(post_report,'interval',seconds =120)
scheduler.start()
