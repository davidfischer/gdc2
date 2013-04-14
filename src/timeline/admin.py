from django.contrib import admin
from models import GithubEvent, Actor, Repository


class GithubEventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'url', 'event_type', 'actor', 'repository')
    list_filter = ('event_type',)
    search_fields = ['url', 'actor__username', 'repository__name']
    list_per_page = 1000


class ActorAdmin(admin.ModelAdmin):
    list_display = ('username', 'actor_type', 'location')
    list_filter = ('actor_type',)
    search_fields = ['username', 'location']
    list_per_page = 1000


class RepsoitoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'owner', 'is_fork', 'language')
    list_filter = ('is_fork', 'language')
    search_fields = ['name', 'owner']
    list_per_page = 1000


admin.site.register(GithubEvent, GithubEventAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Repository, RepsoitoryAdmin)
