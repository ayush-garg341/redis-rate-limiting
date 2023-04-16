from django.shortcuts import render
from django.views import View
from ipware import get_client_ip
from redis import Redis
from django.http import HttpResponse
from rate_limiting import settings
from datetime import timedelta

if settings.REDIS_URL:
    redis_default = Redis.from_url(url=settings.REDIS_URL)
else:
    redis_default = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB
    )

key = 'PING'
limit = 10
period = timedelta(seconds=10)

def request_is_limited(red: Redis, key: str, limit: int, redis_period: timedelta):
    if red.setnx(key, limit):
        red.expire(key, int(redis_period.total_seconds()))
    bucket_val = red.get(key)
    if bucket_val and int(bucket_val) > 0:
        red.decrby(key, 1)
        return False
    return True

class GetPongView(View):
    def get(self, request, *args, **kwargs):
        ip, is_routable = get_client_ip(request)
        if request_is_limited(redis_default, key, limit, period):
            return HttpResponse("Too many requests, please try again later.", status=429)
        return HttpResponse("PONG", 200)



def index(request):
    context = {}
    return render(request, "index.html", context)
