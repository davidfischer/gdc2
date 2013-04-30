import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Count
from django.http import HttpResponse
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

@cache_page(60 * 30)
def language(request, lang='All'):
    events = GithubEvent.objects.filter(
        repository__is_fork=False).exclude(
        actor__location__lat=None).exclude(
        actor__location__lng=None)

    if lang != 'All':
        events.filter(repository__language=lang)
    events.select_related().annotate(Count('actor__location__name'))

    data = [dict(e) for e in events]

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
