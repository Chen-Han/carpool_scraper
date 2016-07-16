from django.core.management.base import BaseCommand, CommandError
from fb_bot.models import Post
from fb_bot.scrape_logic import scraper
from fb_bot import service
from fb_bot import views
from fb_bot import bot

_page_to_scrape = 'http://bbs.uwcssa.com/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=54'
class Command(BaseCommand):
    help = 'scrape pages'
    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        posts = scraper.scrape_page(_page_to_scrape)
        for post in posts:
            saved_post = service.store_post_if_not_exists(post)
            if(saved_post): # post saved i.e. new post
                reminders = service.find_all_reminders(saved_post)
                if(reminders and len(reminders) > 0):
                    for reminder in reminders:
                        views.reply(reminder.fb_user.fb_id,
                            bot.get_post_description(saved_post))

