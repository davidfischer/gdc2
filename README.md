Where does open source come from?
=================================

Sometimes a [picture](http://davidfischer.github.io/gdc2/) is worth a thousand
words.

This interactive visualization of the location of contributors to the
top repositories on GitHub was my entry to the
[GitHub Data Challenge](https://github.com/blog/1450-the-github-data-challenge-ii)


Developing
----------

The provided Makefile has everything needed to fetch data from
[GitHub Archive](http://githubarchive.org), load it into a database,
geocode locations and output the resulting JSON. It can even push
the results to GitHub pages.

There are also some interesting `queries` for doing things like fetching
top 200 repositories, gathering up all the relevant events or getting
the unique set of locations to geocode.

    # This first step takes hours and downloads ~6.5GB
    make githubarchive

    # This step takes a few hours with decently fast disks
    make loaddb

    # This step geocodes any locations not already geocoded (`locations.json`)
    make geocode

    # Generate the `events.json` file used for the visualization
    make jsonify



Credits
-------

* Geocoding by [Nominatim](http://wiki.openstreetmap.org/wiki/Nominatim),
  &copy; OpenStreetMap contributors.

* Inspired by earlier work by [Jens Finnäs](http://jensfinnas.com/dataist/ows/)
  and [Nanda Yadav](http://visual.ly/visualizing-nfl-draft-history)

* Built with [d3](http://d3js.org) by Mike Bostock
