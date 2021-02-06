from annoying.decorators import render_to
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect


@cache_page(60 * 15)
@csrf_protect
@render_to("www/index.html")
def index(request):
    return {}
