from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 30)
def index(request):
    return render(request, 'visualize/index.html')