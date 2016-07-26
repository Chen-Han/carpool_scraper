from django.test import TestCase
import service
from scrape_logic.request_analyzer import RequestInfo
from scrape_logic.location_extractor import TORONTO, WATERLOO
from models import FbUser,Reminder, Post
from datetime import datetime
import pytz

utc=pytz.UTC

class ServiceTestCase(TestCase):
    fb_id = "123456778"
    fb_id2 = "556322266"
    # must make date object time aware
    ref_date = utc.localize(datetime(2015,1,2))
    ref_date1 = utc.localize(datetime(2015,1,1))

    def setUp(self):
        fbuser = FbUser.objects.create(fb_id=ServiceTestCase.fb_id)
        fbuser2 = FbUser.objects.create(fb_id=ServiceTestCase.fb_id2)
        Post.objects.create(original_title="Hello",
            url="https://example",from_location=WATERLOO,
            to_location=TORONTO, scrape_date=ServiceTestCase.ref_date,
            carpool_date=ServiceTestCase.ref_date)
        Post.objects.create(original_title="Hello1",
            url="https://example1.com",from_location=WATERLOO,
            scrape_date = ServiceTestCase.ref_date,
            to_location=TORONTO,carpool_date=ServiceTestCase.ref_date1)
        Reminder.objects.create(from_location=WATERLOO,
            to_location=TORONTO,carpool_date=ServiceTestCase.ref_date,
            fb_user = fbuser)
        Reminder.objects.create(from_location=WATERLOO,
            to_location=TORONTO,carpool_date=ServiceTestCase.ref_date,
            fb_user = fbuser2)

        # Animal.objects.create(name="cat", sound="meow")
        pass

    def test_store_user(self):
        fb_id = "12368885632"
        service.add_user_if_not_exists(fb_id)
        db_user = FbUser.objects.get(fb_id=fb_id)
        self.assertIsNotNone(db_user)
        self.assertEquals(fb_id,db_user.fb_id)

    def test_store_reminder(self):
        from_location = WATERLOO
        to_location = TORONTO
        date = datetime(2015,6,7)
        request_info = RequestInfo(date,from_location,to_location)
        reminder = service.store_reminder(ServiceTestCase.fb_id,request_info)
        self.assertIsNotNone(reminder)
        self.assertEquals(date,reminder.carpool_date)
        self.assertEquals(from_location,reminder.from_location)
        self.assertEquals(to_location,reminder.to_location)

    def test_filter_posts(self):
        from_location = WATERLOO
        to_location = TORONTO
        req_info = RequestInfo(ServiceTestCase.ref_date,from_location,to_location)
        posts = service.filter_carpool_posts(req_info)
        self.assertEquals(1,len(posts))
        self.assertEquals(ServiceTestCase.ref_date,posts[0].carpool_date)
        self.assertEquals(from_location,posts[0].from_location)
        self.assertEquals(to_location,posts[0].to_location)


    def test_store_post_if_not_exists(self):
        # already exists, same url
        post_model = Post.objects.create(original_title="Carpool this Saturday from Waterloo to Toronto",
            url="https://example.com",from_location=WATERLOO,
            scrape_date = ServiceTestCase.ref_date,
            to_location=TORONTO,carpool_date=ServiceTestCase.ref_date)
        self.assertEquals(service.store_post_if_not_exists(post_model),None)
        post_model.url = "https://change_url.com"
        stored_post = service.store_post_if_not_exists(post_model)
        self.assertIsNotNone(stored_post)
        db_post = Post.objects.get(url=post_model.url)
        self.assertEquals(stored_post,db_post)

    def test_find_all_reminders(self):
        post_model = Post.objects.create(original_title="Carpool this Saturday from Waterloo to Toronto",
            url="https://example.com",from_location=WATERLOO,
            scrape_date = ServiceTestCase.ref_date,
            to_location=TORONTO,carpool_date=ServiceTestCase.ref_date)
        reminders = service.find_all_reminders(post_model)
        self.assertEquals(len(reminders),2)
        for reminder in reminders:
            self.assertEquals(reminder.carpool_date,ServiceTestCase.ref_date)
        print("======reminders=====")
        for reminder in reminders:
            print(reminder.fb_user.fb_id)
        
    def test_cancel_reminder(self):
        result = service.cancel_reminder(ServiceTestCase.fb_id)
        self.assertEquals(result,1)
        reminders = Reminder.objects.filter(fb_user_id=ServiceTestCase.fb_id)
        self.assertEquals(len(reminders),0)
        self.assertEquals(service.cancel_reminder(ServiceTestCase.fb_id),0)
