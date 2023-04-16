from django.shortcuts import render
from django.views import View
from ipware import get_client_ip
from redis import Redis
from django.http import HttpResponse
from rate_limiting import settings
import time

if settings.REDIS_URL:
    redis_default = Redis.from_url(url=settings.REDIS_URL)
else:
    redis_default = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    )

key = "PING"
limit = 5
time_window_sec = 60


def request_is_limited(red: Redis, key: str, limit: int, redis_period: int):
    # This all should be atomic operation and under transaction.
    # Locking before updating is crucial in concurrent transactions case.
    get_all = red.hgetall(key)
    epoch = int(time.time())
    total_req = 0
    if get_all:
        start_time = epoch - redis_period
        for k, v in get_all.items():
            if int(k.decode("utf-8")) < start_time:
                red.hdel(key, k)
            else:
                total_req += 1
    if total_req < limit:
        val = red.hget(key, epoch)
        if val:
            val = int(val.decode("utf-8")) + 1
        else:
            val = 1
        red.hset(key, epoch, val)
        return False
    return True


class GetSlidingWindow(View):
    def get(self, request, *args, **kwargs):
        ip, is_routable = get_client_ip(request)
        if request_is_limited(redis_default, key, limit, time_window_sec):
            return HttpResponse(
                "Too many requests, please try again later.", status=429
            )
        return HttpResponse("Success", 200)
