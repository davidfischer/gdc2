from django.db.models import Max
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from timeline.models import GithubEvent


@cache_page(60 * 30)
def index(request):
    return render(request, 'visualize/index.html')

def status(request):
    return render(request,
        'visualize/status.html',
        {
            'latest_event': GithubEvent.objects.aggregate(Max('created_at'))['created_at__max'],
        })