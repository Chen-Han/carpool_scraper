import scrape_page
from fb_bot.models import FbUser,Reminder, Post
from django.test import TestCase
from datetime import datetime
import pytz

utc=pytz.UTC

class TestScrapePageCommand(TestCase):
    def setUp(self):
        fb_user = FbUser.objects.create(fb_id="1050205258396486")
        reminder = Reminder.objects.create(from_location="Waterloo",to_location="Toronto",carpool_date=datetime(2016,7,27),fb_user=fb_user)

    def test_scrape_page(self):
        saved_post = Post.objects.create(from_location="Waterloo",scrape_date=datetime(2016,7,26), url="https://example.com",original_title="hi..",to_location="Toronto",carpool_date=datetime(2016,7,27))
        scrape_page.remind_users(saved_post)
        # expect to receive a message, check fb here
