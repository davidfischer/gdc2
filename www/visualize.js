/*jslint browser: true, vars: true, white: true, indent: 2 */

$(document).ready(function() {
  "use strict";

  var LANGUAGES = [
    "All",
    "JavaScript",
    "Ruby",
    "Python",
    "PHP",
    "Shell",
    "Java",
    "Objective-C",
    "C++",
    "C"
  ], REPOSITORIES = [
    "",
    "twitter/bootstrap",
    "octocat/Spoon-Knife",
    "mxcl/homebrew",
    "rails/rails",
    "h5bp/html5-boilerplate",
    "jquery/jquery",
    "saasbook/hw3_rottenpotatoes",
    "joyent/node",
    "robbyrussell/oh-my-zsh",
    "phonegap/phonegap-start",
    "bartaz/impress.js",
    "documentcloud/backbone",
    "mbostock/d3",
    "torvalds/linux",
    "saasbook/hw4_rottenpotatoes",
    "purplecabbage/phonegap-plugins",
    "github/gitignore",
    "wakaleo/game-of-life",
    "EllisLab/CodeIgniter",
    "symfony/symfony",
    "jquery/jquery-ui",
    "mrdoob/three.js",
    "django/django",
    "harvesthq/chosen",
    "phonegap/phonegap-plugins",
    "blueimp/jQuery-File-Upload",
    "imathis/octopress",
    "hakimel/reveal.js",
    "zendframework/zf2",
    "zurb/foundation",
    "diaspora/diaspora",
    "jquery/jquery-mobile",
    "mojombo/jekyll",
    "angular/angular.js",
    "gitlabhq/gitlabhq",
    "mathiasbynens/dotfiles",
    "fdv/typo",
    "TrinityCore/TrinityCore",
    "adobe/brackets",
    "git/git",
    "AFNetworking/AFNetworking",
    "addyosmani/todomvc",
    "cloudhead/less.js",
    "spree/spree",
    "facebook/facebook-php-sdk",
    "plataformatec/devise",
    "saasbook/typo",
    "FortAwesome/Font-Awesome",
    "JakeWharton/ActionBarSherlock",
    "facebook/three20"
  ];

  var width = 960, height = 500;

  var projection = d3.geo.wagner6()
      .scale(150);

  var path = d3.geo.path()
      .projection(projection);

  var graticule = d3.geo.graticule();

  var svg = d3.select("#vis").append("svg")
      .attr("width", width)
      .attr("height", height);

  var allscale = d3.scale.log().domain([1, 500]).range([2, 15]);

  svg.append("defs").append("path")
      .datum({type: "Sphere"})
      .attr("id", "sphere")
      .attr("d", path);

  svg.append("use")
      .attr("class", "stroke")
      .attr("xlink:href", "#sphere");

  svg.append("use")
      .attr("class", "fill")
      .attr("xlink:href", "#sphere");

  svg.append("path")
      .datum(graticule)
      .attr("class", "graticule")
      .attr("d", path);

  d3.json("world-110m.json", function(world) {
    svg.insert("path", ".graticule")
        .datum(topojson.object(world, world.objects.land))
        .attr("class", "land")
        .attr("d", path);

    svg.insert("path", ".graticule")
        .datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
        .attr("class", "boundary")
        .attr("d", path);
  });

  var tooltip = d3.select("body").append("div")
      .attr("id", "tooltip")
      .style("display", "none")
      .style("position", "absolute")
      .html(["<p id=\"tt_location\"><label>Location:</label><span id=\"tt_location_value\"></span></p>",
             "<p id=\"tt_contributions\"><label>Contributions:</label><span id=\"tt_contributions_value\"></span></p>",
             "<p id=\"tt_contributors\"><label>Top contributors:</label><span id=\"tt_contributors_value\"></span></p>"].join("")
      )

  // Load languages into clickable links
  d3.select("#language-list").selectAll("li")
    .data(LANGUAGES).enter()
    .append("li")
      .attr("class", function(d) { return d === "All" ? "active" : ""; })
    .append("a")
      .attr("href", function(d) { return "#languages/" + d.replace(/\+/g, "_"); })
      .text(function(d) { return d; })
      .attr("id", function(d) { return "languages-" + d.replace(/\+/g, "_"); })
      .on("click", function() {
        $("#language-list li").removeClass("active");
        $(this).parent().addClass("active");
        return true;
      });

  // Load repositories into a select input
  d3.select("#repository-list")
    .on("change", function() {
        window.location.hash = "#repositories/" + $(this).val();
      })
    .selectAll("option")
    .data(REPOSITORIES).enter()
    .append("option")
      .attr("value", function(d) { return d; })
      .text(function(d) { return d; });

  $("#filter-selector button").on("click", function() {
    $(".radio-filter").hide();
    $("#" + $(this).attr("data-elem")).show();
  });

  var getlang = function() {
    var langregex = /^\#languages\/([a-zA-Z0-9\-\+\.]+)$/;
    var langres = langregex.exec(window.location.hash);

    if (langres !== null) {
      return langres[1];
    }
    return null;
  };

  var getrepo = function() {
    // TODO: doens't handle unicode/weird names at all
    var reporegex = /^\#repositories\/([a-zA-Z0-9\-\+\.\/]+)$/;
    var repores = reporegex.exec(window.location.hash);

    if (repores !== null) {
      return repores[1];
    }
    return null;
  }

  
  
  var hashchangehandler = function() {
    var lang = getlang();
    var repo = getrepo();

    $("#filter-selector button").removeClass("active");
    if (lang !== null) {
      $("#language-btn").trigger('click');
      $("#language-list li").removeClass("active");
      $("#languages-" + lang.replace(/\+/g, "_")).parent().addClass("active");
    } else if (repo !== null) {
      $("#repository-btn").trigger('click');
      $("#repository-list").val(repo);
    } else {
      // Invalid anchor!
      return;
    }

    var contributions = function (d) {
      var lang = getlang(), repo = getrepo();
      var sum = 0, key;

      if (lang !== null && lang !== "All") {
        return lang in d["languages"] ? d["languages"][lang] : 0;
      } else if (repo !== null) {
        return repo in d["repositories"] ? d["repositories"][repo] : 0;
      }

      for (key in d['repositories']) {
        sum += d['repositories'][key];
      }
      return sum;
    };

    var scaler = function(d) {
      var contribs = contributions(d);
      return contribs > 0 ? allscale(contribs) : 0;
    }


    if ($("circle.dot").length > 0) {
      svg.selectAll("circle.dot")
        .transition()
        .attr("r", scaler);
    } else {
      d3.json("data/events.json", function (data) {
        svg.selectAll(".dots")
          .data(data).enter()
          .append("circle")
          .attr("class", "dot")
          .attr("r", scaler)
          .attr("transform", function(d) {
            var coord = [d['lng'], d['lat']];
            return "translate(" + projection(coord).join(",") + ")";
          })
          .on("mouseover", function(d) {
            var m = d3.mouse(d3.select("body").node());
            tooltip.style("display", null)
                .style("left", m[0] + 30 + "px")
                .style("top", m[1] - 20 + "px");
            $("#tt_location_value").text(d["name"]);
            $("#tt_contributions_value").text(contributions(d));
            if (getlang() === "All") {
              $("#tt_contributors").show();
              $("#tt_contributors_value").text(d["users"].join(", "));
            } else {
              $("#tt_contributors").hide();
            }
            })
            .on("mouseout", function() {
              tooltip.style("display", "none");
            });
      });
    }
  };
  $(window).on("hashchange", hashchangehandler);


  // Default page to load is all languages
  if (window.location.hash === "") {
    window.location.hash = "#languages/All";
  } else {
    hashchangehandler();
  }

});