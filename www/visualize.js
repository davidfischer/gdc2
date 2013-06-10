/*jslint browser: true, vars: true, white: true, indent: 2 */

$(document).ready(function() {
  "use strict";

  var LANGUAGES = [
    "All",
  ], REPOSITORIES = [
    "",
    "mono/MonoGame",
    "SignalR/SignalR",
    "mono/mono",
    "monospider/monogame",
    "ServiceStack/ServiceStack",
    "gmy77/d3sharp",
    "jagregory/fluent-nhibernate",
    "restsharp/RestSharp",
    "ravendb/ravendb",
    "NancyFx/Nancy",
    "hbons/SparkleShare",
    "gitextensions/gitextensions",
    "pubnub/pubnub-api",
    "AutoMapper/AutoMapper",
    "mono/monodevelop",
    "xamarin/monodroid-samples",
    "nhibernate/nhibernate-core",
    "Redth/PushSharp",
    "ServiceStack/ServiceStack.Text",
    "SamSaffron/dapper-dot-net",
    "DotNetOpenAuth/DotNetOpenAuth",
    "robconery/massive",
    "ligershark/webdevchecklist.com",
    "schambers/fluentmigrator",
    "mongodb/mongo-csharp-driver",
    "subsonic/SubSonic-3.0",
    "xamarin/mobile-samples",
    "SamSaffron/MiniProfiler",
    "NServiceBus/NServiceBus",
    "MahApps/MahApps.Metro",
    "ninject/ninject",
    "phatboyg/MassTransit",
    "facebook-csharp-sdk/facebook-csharp-sdk",
    "DarthFubuMVC/fubumvc",
    "xamarin/monotouch-samples",
    "toptensoftware/PetaPoco",
    "ServiceStack/ServiceStack.Redis",
    "migueldeicaza/MonoTouch.Dialog",
    "mausch/SolrNet",
    "joliver/EventStore",
    "koush/sqlite-net",
    "icsharpcode/ILSpy",
    "ServiceStack/ServiceStack.OrmLite",
    "chrisforbes/OpenRA",
    "machine/machine.specifications",
    "dotless/dotless",
    "Jessecar96/SteamBot",
    "mono/monotouch-bindings",
    "markrendle/Simple.Data",
    "JamesNK/Newtonsoft.Json",
  ];

  var width = 960, height = 500;

  var projection = d3.geo.wagner6()
      .scale(150);

  var path = d3.geo.path()
      .projection(projection);

  var graticule = d3.geo.graticule();

  var svg = d3.select("#vis").append("svg")
      .attr("width", width)
      .attr("height", height)
      .call(d3.behavior.zoom()
        .scaleExtent([150, 1000])
        .translate(projection.translate())
        .scale(projection.scale())
        .on("zoom", redraw));

  var allscale = d3.scale.log().domain([1, 500]).range([3, 20]);

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
      .html(["<p><label>Location:</label><span id=\"tt_location_value\"></span></p>",
             "<p><label>Contributions:</label><span id=\"tt_contributions_value\"></span></p>",
             "<p class=\"tt_all_only\"><label>Top contributors:</label><span id=\"tt_contributors_value\"></span></p>",
             "<p class=\"tt_all_only\"><label>Top repositories:</label><span id=\"tt_repositories_value\"></span></p>",
             "<p class=\"tt_all_only\"><label>Top languages:</label><span id=\"tt_languages_value\"></span></p>"].join("")
      );

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


  var hashchangehandler = function() {
    var getlang = function() {
      var langregex = /^\#languages\/([a-zA-Z0-9\-\+\_\.]+)$/;
      var langres = langregex.exec(window.location.hash);

      if (langres !== null) {
        return langres[1];
      }
      return null;
    };

    var getrepo = function() {
      // TODO: doens't handle non-ascii names at all
      var reporegex = /^\#repositories\/([a-zA-Z0-9\-\_\+\.\/]+)$/;
      var repores = reporegex.exec(window.location.hash);

      if (repores !== null) {
        return repores[1];
      }
      return null;
    };

    $("#filter-selector button").removeClass("active");
    if (getlang() !== null) {
      $("#language-btn").trigger('click');
      $("#language-list li").removeClass("active");
      $("#languages-" + getlang()).parent().addClass("active");
    } else if (getrepo() !== null) {
      $("#repository-btn").trigger('click');
      $("#repository-list").val(getrepo());
    } else {
      // Invalid anchor!
      return;
    }

    var contributions = function (d) {
      var lang = getlang(), repo = getrepo();
      var sum = 0, key;

      if (lang !== null && lang !== "All") {
        lang = lang.replace(/_/g, "+");
        return lang in d["languages"] ? d["languages"][lang] : 0;
      } else if (repo !== null) {
        return repo in d["repositories"] ? d["repositories"][repo] : 0;
      }

      for (key in d['languages']) {
        sum += d['languages'][key];
      }
      return sum;
    };

    var scaler = function(d) {
      var contribs = contributions(d);
      return contribs > 0 ? allscale(contribs) : 0;
    };

    // Returns top 3 keys in an object by comparing numeric values
    var topthree = function(d) {
      var sortable = [];
      for (var r in d) {
        sortable.push([r, d[r]]);
      }
      sortable = sortable.sort(function(a, b) {return b[1] - a[1]}).slice(0, 3);

      return $.map(sortable, function(o) {
        var re = /^[^\/]+\//
        return o[0].replace(re, "");
      });
    };


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
              $(".tt_all_only").show();
              $("#tt_contributors_value").text(d["users"].join(", "));

              // top repositories
              $("#tt_repositories_value").text(topthree(d["repositories"]).join(", "));
              $("#tt_languages_value").text(topthree(d["languages"]).join(", "));
            } else {
              $(".tt_all_only").hide();
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

  function redraw() {
    if (d3.event) {
      projection
          .translate(d3.event.translate)
          .scale(d3.event.scale);
    }

    // Redraw circles!
    d3.selectAll("circle.dot")
        .attr("transform", function(d) {
          var coord = [d['lng'], d['lat']];
          return "translate(" + projection(coord).join(",") + ")";
        });

    svg.selectAll("path").attr("d", path);
    var t = projection.translate();
  }


});
