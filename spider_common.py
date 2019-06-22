import urllib.request, urllib.error, urllib.parse
import config


def gen_req(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req


def dprint(flag, *args, **kwargs):
    if flag:
        print(*args, **kwargs)


def tprint(*args, **kwargs):
    if config.Testing:
        print(*args, **kwargs)
