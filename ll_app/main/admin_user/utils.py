from urllib.parse import urlparse, urljoin
from flask import request, url_for
import random

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def pop_rand(a_list):
    index = random.randrange(0, len(a_list))
    return a_list.pop(index)
