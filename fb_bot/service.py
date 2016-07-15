"""Main service to interact with database models"""


def add_user_if_not_exists(fb_id):
    pass

def store_reminder(fb_id,request_info):
    pass

def filter_carpool_requests(request_info):
    pass

def cancel_reminder(fb_id):
    pass

#given a post object (not a model)
def store_post_if_not_exists(post):
    return #Post_model if post is new, else return false

#find all reminder that is looking for a carpool post like `post``
# return a list of reminder objects
def find_all_reminder(post_model):
    # for all reminders
    # if reminder matches post and post_model, return the reminder
    return [] 

# after thinking, this might not be needed
# given a post model, a fb user model
# mark the post as seen by the user
# def mark_as_seen(post_model,fb_user_model):
#     pass

