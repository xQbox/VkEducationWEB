from django.core.management import BaseCommand
from app.models import Profile, Question, Tag
from django.core.cache import cache

CACHE_TTL = 1 * 24 * 60 * 60    # 1 day

class Command(BaseCommand):
    help = "Updates cache of the side bar"

    def handle(self, *args, **kwargs):
        data = Profile.objects.get_top_users()
        cache.set('top_users', data, CACHE_TTL)

        data = Tag.objects.get_popular()
        cache.set('top_tags', data, CACHE_TTL)

        print("Cache was successfully refreshed!")
        