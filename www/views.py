from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from fbv.decorators import render_html


@cache_page(60 * 15)
@csrf_protect
@render_html("www/index.html")
def index(request):
    return {}
