.PHONY: githubarchive tests loaddb


all: tests


# Must have required Python packages
loaddb:
	@echo "Loading githubarchive data into local database."
	@echo "One month of data takes about one hour on my SSD."
	python gdc2/loaddb.py


githubarchive:
	@echo "Downloading githubarchive.org data. This takes hours."
	mkdir -p githubarchive

	# Requires bash 4+ MacOS users may need to update or something
	cd githubarchive && wget http://data.githubarchive.org/2013-{01..04}-{01..31}-{0..23}.json.gz


tests:
	nosetests
