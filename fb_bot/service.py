"""Main service to interact with database models"""
from models import FbUser,Post,Reminder

def add_user_if_not_exists(fb_id):
    return FbUser.objects.get_or_create(fb_id=fb_id)


def store_reminder(fb_id,request_info):
    fb_user = FbUser.objects.get(fb_id=fb_id)
    reminder = fb_user.reminder_set.create(from_location=request_info.from_location,
        to_location=request_info.to_location,carpool_date = request_info.date)
    return reminder


def filter_carpool_posts(request_info):
    posts = Post.objects.filter(carpool_date=request_info.date, 
        from_location=request_info.from_location,
        to_location=request_info.to_location)
    return posts

def cancel_reminder(fb_id):
    reminders = FbUser.objects.get(fb_id=fb_id).reminder_set.all()
    length = len(reminders)
    reminders.delete()
    # if(length>0):
    #     for r in reminders:
    #         r.delete()
    return length

#given a post object (not a model)
# return none if exists
def store_post_if_not_exists(post_model):
    matching_post = Post.objects.filter(url=post_model.url)
    if(len(matching_post) == 0):
        post_model.save()
        return post_model
    else:
        return None

#find all reminder that is looking for a carpool post like `post``
# return a list of reminder objects
def find_all_reminders(post_model):
    # for all reminders
    # if reminder matches post and post_model, return the reminder
    matching_reminders = Reminder.objects.filter(from_location=post_model.from_location,
        to_location=post_model.to_location,
        carpool_date=post_model.carpool_date)
    return matching_reminders

# after thinking, this might not be needed
# given a post model, a fb user model
# mark the post as seen by the user
# def mark_as_seen(post_model,fb_user_model):
#     pass

