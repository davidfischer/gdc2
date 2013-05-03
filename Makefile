.PHONY: locations alllanguages languages repositories githubarchive tests

REPOSITORIES = rails/rails
LANGUAGES = JavaScript Ruby Java Python Shell PHP C C++ Perl Objective-C


all: alllanguages languages repositories

locations:
	@echo "Fetching location data. This takes hours if this is the first time"
	python scripts/github-data-fetch.py --locations --outfile www/data/locations.json

alllanguages:
	@echo "Fetching data for all languages"
	python scripts/github-data-fetch.py --outfile www/data/languages/All.json

languages:
	@echo "Fetching language data"
	for lang in $(LANGUAGES); do \
		python scripts/github-data-fetch.py --language $$lang --outfile www/data/languages/$$lang.json ; \
	done

repositories:
	@echo "Fetching data for repositories"
	for repo in $(REPOSITORIES); do \
		
		python scripts/github-data-fetch.py --repo $$repo --outfile www/data/repositories/$$repo.json ; \
	done

githubarchive:
	@echo "Downloading githubarchive.org data"
	mkdir -p githubarchive

	# Requires bash 4+ MacOS users may need to update
	cd githubarchive && wget http://data.githubarchive.org/2013-{01..04}-{01..31}-{0..23}.json.gz

tests:
	nosetests