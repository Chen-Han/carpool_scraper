# -*- coding: utf-8 -*-
import random
import re
from .scrape_logic import request_analyzer

"""
bot-related logic, including how to reply message, how to extract
info from a message etc
Commands:
Help # which prints help message
Show on [DATE] [Waterloo/Toronto] to [Toronto/Waterloo]
# TODO Show from [DATE] to [DATE] [Waterloo/Toronto] to [Toronto/Waterloo]
# TODO Show on [DATE1], [DATE2] ... [Waterloo/Toronto] to [Toronto/Waterloo]
Remind on [Date] [Waterloo/Toronto] to [Toronto/Waterloo]
Cancel reminder
"""

# -*- coding: utf-8 -*-
import util
_error_messages = ["oops, 老司机的车抛锚了，请再次尝试","系统故障，500"]

def get_error_message():
    i = random.randint(0,len(_error_messages)-1)
    return _error_messages[i]

def get_reminder_set_message(request_info):
    return ("You are looking for carpool on " + 
        util.format_date(request_info.date) + " from " + 
        request_info.from_location + " to " +
        request_info.to_location + "\n" +
        "Type cancel reminder to cancel it any time.")

def get_not_recognized_command_message():
    return "bi bi bi bi bi bi, command not recognized"

def get_invalid_request_info_message():
    return ("Does not look like have a valid request info, sample request: "+
            "show on July 24 from Waterloo to Toronto. which lists all Waterloo to Toronto carpools")

def get_help_message():
    return ("Thank you for asking, type help to view this message again. You can filter all carpool posts by "+
        "typing \n 'show on July 24 from Toronto to Waterloo' \n"+
        "or set a reminder when a carpool post comes out\n"+
        "'remind on July 29 from Waterloo to Toronto' \n"+
        "as of this version, the only locations supported are Waterloo and Toronto")

def get_post_description(post_model):
    return (post_model.original_title + " \n" + 
        "Phone: " + post_model.phone + "\n" + 
        "URL: " + post_model.url)

# return a new line separated post list
def get_post_list_message(post_model_list):
    return ("=====Carpool List ("+ len(post_model_list)+")=====" + 
        ("\n".join([get_post_list_message(i) for i in post_model_list])))

def get_cancel_reminder_message(success):
    if(success):
        return "Your reminder is canceled"
    else:
        return "You did not set a reminder, cannot cancel"

_cancel_re = re.compile('^cancel reminder')
_show_re = re.compile('^show')
_remind_re = re.compile('^remind')
_help_re = re.compile('^help')

# given a user message, and facebook id, dispatch it to various action
# generate a response
def get_response(msg,fb_id):
    msg = msg.strip().lower() #normalize
    # service.add_user_if_not_exists(fb_id)
    if(len(msg)==0):
        return "Sorry, I did not receive your message. Try again?"
    if(_help_re.match(msg)):
        return get_help_message()
    if (_cancel_re.match(msg)):
        # perform cancel
        return "Cancel success or fail"

    request_info = request_analyzer.parse_request(msg)
    show_result = _show_re.match(msg)
    if (show_result and request_info):
        # after request info, call service to load data
        return "TODO, show you the result"
    elif(show_result):
        return get_invalid_request_info_message()

    remind_result = _remind_re.match(msg)
    if (remind_result and request_info):
        # send to service
        return get_reminder_set_message(request_info)
    elif (remind_result):
        return get_invalid_request_info_message()
    return get_not_recognized_command_message()


