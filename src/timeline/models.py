from django.db import models
from dateutil.parser import parse


class GetAndUpdateManager(models.Manager):
    def get_and_update_or_create(self, unique_fields, update_fields):
        '''
        Looks up an object with unique_fields and updates it if any update_fields
        are changed
        Creates the object if it does not exist
        Returns a tuple of (object, created), where created is a boolean
        specifying whether an object was created.
        '''

        try:
            instance = self.get(**unique_fields)
        except self.model.DoesNotExist:
            params = dict([(k, v) for k, v in unique_fields.items()])
            params.update(update_fields)
            instance = self.model(**params)
            instance.save(force_insert=True)
            return instance, True

        save_reqd = False
        for key in update_fields:
            if getattr(instance, key) != update_fields[key]:
                save_reqd = True
                setattr(instance, key, update_fields[key])

        if save_reqd:
            instance.save()

        return instance, False


class Repository(models.Model):
    url = models.CharField(max_length=1024, unique=True)
    name = models.CharField(max_length=1024, db_index=True)

    # The owner is not guaranteed to be in the Actor table
    owner = models.CharField(max_length=1024, db_index=True)
    is_fork = models.NullBooleanField(default=None, blank=True)
    language = models.CharField(max_length=1024, null=True, default=None, blank=True, db_index=True)

    # Fields to keep track of when data was imported
    dbentry_create_date = models.DateTimeField(auto_now_add=True)
    dbentry_mod_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = GetAndUpdateManager()

    def github_url(self):
        return 'https://github.com/{0}/{1}'.format(self.owner, self.name)

    def __unicode__(self):
        return self.name

    @staticmethod
    def from_archive(archive):
        def handle_isfork(is_fork):
            if isinstance(is_fork, basestring):
                if is_fork.lower() == 'true':
                    return True
                elif is_fork.lower() == 'false':
                    return False
                return None
            return is_fork

        url = archive.get('url')
        name = archive.get('name')
        owner = archive.get('owner')

        if None not in (url, name, owner) and  '' not in (url, name, owner):
            repository, created = Repository.objects.get_and_update_or_create(
                    unique_fields = {
                        'url': url,
                    },
                    update_fields = {
                        'name': name,
                        'owner': owner,
                        'language': archive.get('language'),
                        'is_fork': handle_isfork(archive.get('fork')),
                    },
                )
            return repository

    class Meta:
        verbose_name_plural = "repositories"


class Actor(models.Model):
    username = models.CharField(max_length=1024, unique=True)
    gravatar_id = models.CharField(max_length=1024, null=True, default=None, blank=True)
    actor_type = models.CharField(max_length=1024, null=True, default=None, blank=True)
    location = models.CharField(max_length=1024, null=True, default=None, blank=True, db_index=True)

    # Fields to keep track of when data was imported
    dbentry_create_date = models.DateTimeField(auto_now_add=True)
    dbentry_mod_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = GetAndUpdateManager()

    def gravatar_url(self, size=40):
        grav_id = self.gravatar_id or '0'
        return 'https://secure.gravatar.com/avatar/{0}.jpg?size={1}'.format(grav_id, size)

    def github_url(self):
        return 'https://github.com/{0}'.format(self.username)

    def __unicode__(self):
        return self.username

    @staticmethod
    def from_archive(archive):
        username = archive.get('login')

        if username is not None and username.strip() != '':
            actor, created = Actor.objects.get_and_update_or_create(
                    unique_fields = {
                        'username': username,
                    },
                    update_fields = {
                        'gravatar_id': archive.get('gravatar_id'),
                        'actor_type': archive.get('type'),
                        'location': archive.get('location'),
                    },
                )
            return actor


class GithubEvent(models.Model):
    created_at = models.DateTimeField(db_index=True)
    url = models.CharField(max_length=1024, null=True, default=None, blank=True)
    event_type = models.CharField(max_length=1024, null=True, default=None, blank=True)

    repository = models.ForeignKey(Repository)
    actor = models.ForeignKey(Actor)

    # Fields to keep track of when data was imported
    dbentry_create_date = models.DateTimeField(auto_now_add=True)
    dbentry_mod_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return unicode(self.url)

    def github_url(self):
        return self.url

    @staticmethod
    def from_archive(archive):
        repository = Repository.from_archive(archive.get('repository', {}))
        actor = Actor.from_archive(archive.get('actor_attributes', {}))

        created_at = archive.get('created_at')

        # Skip records that do not pertain to a repository
        # or an actor or have an invalid date
        if repository is not None and actor is not None and \
            created_at is not None and created_at.strip() != '':

            event = GithubEvent(
                    created_at = parse(created_at),
                    url = archive.get('url'),
                    event_type = archive.get('type'),
                    actor = actor,
                    repository = repository,
                )
            event.save()
            return event
