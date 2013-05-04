from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class GitHubEvent(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    created_at = Column(String, index=True)
    type = Column('type', String, index=True)
    actor = Column('actor', String)
    actor_attributes_login = Column(String)
    actor_attributes_type = Column(String)
    actor_attributes_gravatar_id = Column(String)
    actor_attributes_location = Column(String, index=True)
    repository_name = Column(String)
    repository_url = Column(String, index=True)
    repository_fork = Column(Boolean)
    repository_language = Column(String, index=True)
    repository_forks = Column(Integer)
    repository_stargazers = Column(Integer)
    repository_watchers = Column(Integer)

    def __init__(self, **kwargs):
        for k in kwargs:
            if isinstance(kwargs[k], basestring):
                kwargs[k].strip()
            setattr(self, k, kwargs[k])