from django.db import models

# Create your models here.

class Post(models.Model):
    original_title = models.CharField(max_length=100)
    url = models.CharField(max_length=255,unique=True)
    scrape_date = models.DateTimeField()
    phone = models.CharField(max_length=20)
    from_location = models.CharField(max_length=20)
    to_location = models.CharField(max_length=20)
    carpool_date = models.DateTimeField()


class FbUser(models.Model):
    fb_id = models.CharField(max_length=20,unique=True)
    seen_posts = models.ManyToManyField(Post)

class Reminder(models.Model):
    from_location = models.CharField(max_length=20)
    to_location = models.CharField(max_length=20)
    carpool_date = models.DateTimeField()
    fb_user = models.ForeignKey(FbUser,on_delete=models.CASCADE)

