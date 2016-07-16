from django.test import TestCase
import service
from models import FbUser,Reminder, Post
import pytz
import bot
import re
from datetime import datetime
from scrape_logic.location_extractor import TORONTO,WATERLOO
class BotTestCase(TestCase):
    def test_intergration(self):
        fb_id = "5536222"
        Post.objects.create(original_title="hello",url="https://bbs.uwcssa.ca/",
            from_location=WATERLOO,to_location=TORONTO,
            carpool_date=datetime(2016,12,28),
            phone="2261231234",scrape_date=datetime(2016,12,27))
        msg = " Show me all carpools on Dec 28th from Waterloo to Toronto"
        show_carpool_response = (bot.get_response(msg,fb_id)) # join a list of messages
        print("==========",show_carpool_response)
        show_carpool_response="\n".join(show_carpool_response)
        self.assertIsNotNone(re.search("2261231234",show_carpool_response))
        self.assertIsNotNone(FbUser.objects.get(fb_id=fb_id))

        print(bot.get_response(" Remind me for July 29th from Toronto to Waterloo",fb_id))
        cancel_response = bot.get_response("cancel reminder",fb_id)
        print(cancel_response)
        self.assertIsNotNone(re.search("Cancelled",cancel_response))
        self.assertIsNotNone(re.search("No reminders",bot.get_response("cancel reminder",fb_id)))
    