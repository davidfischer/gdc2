import os
import logging
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, GitHubEvent
from archiveparser import GitHubArchiveParser

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load the database with downloaded data')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    if args.verbose > 0:
        echo = True
    else:
        echo = False

    engine = create_engine('sqlite:///github-events.db', echo=echo)
    Base.metadata.create_all(engine)  # creates if not exists
    Session = sessionmaker(bind=engine)
    session = Session()

    ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../githubarchive')

    for fn in os.listdir(ROOT_DIR):
        if fn.endswith('.json.gz'):
            path = os.path.join(ROOT_DIR, fn)
            print("Loading: {0}".format(path))
            archive = GitHubArchiveParser(path)
            session.add_all([GitHubEvent(**obj) for obj in archive.parse()])
            session.commit()