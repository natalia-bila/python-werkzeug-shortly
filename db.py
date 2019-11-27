from utils import base36_encode


def insert_url(redis, url):
    short_id = redis.get("reverse-url:" + url)
    if short_id is not None:
        return short_id
    url_num = redis.incr("last-url-id")
    short_id = base36_encode(url_num)
    redis.set("url-target:" + short_id, url.encode('utf-8'))
    redis.set("reverse-url:" + url, short_id)
    return short_id


def get_url(redis, short_id):
    return redis.get("url-target:" + short_id).decode('utf-8')


def increment_url(redis, short_id):
    redis.incr("click-count:" + short_id)


def get_count(redis, short_id):
    return int(redis.get("click-count:" + short_id) or 0)


def get_list_urls(redis):
    number_of_urls = int(redis.get("last-url-id") or 0)
    list_urls = []
    for url_number in range(1,number_of_urls+1):
        short_id = base36_encode(url_number)
        list_urls.append((short_id, redis.get("url-target:" + short_id).decode('utf-8')))
    return list_urls

