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
    "spree/spree",
    "cloudhead/less.js",
    "facebook/facebook-php-sdk",
    "plataformatec/devise",
    "FortAwesome/Font-Awesome",
    "JakeWharton/ActionBarSherlock",
    "facebook/three20",
    "douglascrockford/JSON-js",
    "antirez/redis",
    "visionmedia/express",
    "textmate/textmate",
    "carhartl/jquery-cookie",
    "facebook/facebook-ios-sdk",
    "documentcloud/underscore",
    "cakephp/cakephp",
    "emberjs/ember.js",
    "xbmc/xbmc",
    "necolas/normalize.css",
    "github/game-off-2012",
    "facebook/php-sdk",
    "progit/progit",
    "LearnBoost/socket.io",
    "laravel/laravel",
    "gregbell/active_admin",
    "discourse/discourse",
    "facebook/tornado",
    "ajaxorg/ace",
    "CocoaPods/Specs",
    "bigbluebutton/bigbluebutton",
    "Shopify/active_merchant",
    "github/markup",
    "mailchimp/Email-Blueprints",
    "mangos/server",
    "mangos/MaNGOS-Foundation",
    "mitsuhiko/flask",
    "browsermedia/browsercms",
    "facebook/facebook-android-sdk",
    "learnstreet-dev/learnstreet",
    "thoughtbot/paperclip",
    "uavana/android",
    "midgetspy/Sick-Beard",
    "jfeinstein10/SlidingMenu",
    "Bukkit/CraftBukkit",
    "RestKit/RestKit",
    "meteor/meteor",
    "yiisoft/yii",
    "KellyMahan/android_frameworks_base",
    "Widen/fine-uploader",
    "Modernizr/Modernizr",
    "wbond/package_control_channel",
    "ivaynberg/select2",
    "valums/file-uploader",
    "remy/html5demos",
    "SpringSource/spring-framework",
    "sferik/rails_admin",
    "resque/resque",
    "playframework/Play20",
    "pokeb/asi-http-request",
    "refinery/refinerycms",
    "technomancy/emacs-starter-kit",
    "jdg/MBProgressHUD",
    "OpenGG/OpenGG",
    "github/hubot-scripts",
    "ruby/ruby",
    "daneden/animate.css",
    "defunkt/resque",
    "mozilla/pdf.js",
    "bitcoin/bitcoin",
    "kohsuke/hudson",
    "kennethreitz/requests",
    "nathanmarz/storm",
    "ajaxorg/cloud9",
    "sintaxi/phonegap",
    "janl/mustache.js",
    "moodle/moodle",
    "jashkenas/coffee-script",
    "cocos2d/cocos2d-x",
    "opscode/cookbooks",
    "bmizerany/sinatra",
    "elasticsearch/elasticsearch",
    "symfony/symfony-docs",
    "reddit/reddit",
    "mongoid/mongoid",
    "neo/ruby_koans",
    "mongodb/mongo",
    "libgdx/libgdx",
    "php/php-src",
    "Leaflet/Leaflet",
    "WordPress/WordPress",
    "boto/boto",
    "github/hubot",
    "opscode/chef",
    "edgecase/ruby_koans",
    "retlehs/roots",
    "scottjehl/Respond",
    "svenfuchs/rails-i18n",
    "fog/fog",
    "Khan/khan-exercises",
    "TTimo/doom3.gpl",
    "ariya/phantomjs",
    "Bukkit/Bukkit",
    "tobi/delayed_job",
    "holman/dotfiles",
    "github/github-services",
    "JakeWharton/Android-ViewPagerIndicator",
    "mozilla/BrowserQuest",
    "rapid7/metasploit-framework",
    "github/android",
    "mitchellh/vagrant",
    "lockitron/selfstarter",
    "wildfly/wildfly",
    "nnnick/Chart.js",
    "jbossas/jboss-as",
    "eternicode/bootstrap-datepicker",
    "addyosmani/backbone-fundamentals",
    "rs/SDWebImage",
    "jzaefferer/jquery-validation",
    "thomasdavis/backbonetutorials",
    "mozilla-b2g/gaia",
    "madrobby/zepto",
    "divio/django-cms",
    "olton/Metro-UI-CSS",
    "BradLarson/GPUImage",
    "doctrine/doctrine2",
    "chriseppstein/compass",
    "edavis10/redmine",
    "johnezang/JSONKit",
    "timrwood/moment",
    "cocos2d/cocos2d-iphone",
    "android/platform_frameworks_base",
    "arduino/Arduino",
    "chriskempson/tomorrow-theme",
    "Netflix/Cloud-Prize",
    "facebook/hiphop-php",
    "DmitryBaranovskiy/raphael",
    "mono/MonoGame",
    "altercation/solarized",
    "angular/angular-seed",
    "venomous0x/WhatsAPI",
    "mleibman/SlickGrid",
    "toastdriven/django-tastypie",
    "SignalR/SignalR",
    "desandro/masonry",
    "carlhuda/bundler",
    "ryanb/dotfiles",
    "daproy/android_packages_apps_Settings",
    "marijnh/CodeMirror",
    "astaxie/build-web-application-with-golang",
    "loopj/jquery-tokeninput",
    "blasten/turn.js",
    "visionmedia/jade",
    "seajs/seajs",
    "pyrocms/pyrocms",
    "nvie/gitflow",
    "cucumber/cucumber",
    "appcelerator/titanium_mobile",
    "zencoder/video-js",
    "fatfreecrm/fat_free_crm",
    "jnicklas/capybara"
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
             "<p id=\"tt_contributors\"><label>Top contributors:</label><span id=\"tt_contributors_value\"></span></p>",
             "<p id=\"tt_repositories\"><label>Top repositories:</label><span id=\"tt_repositories_value\"></span></p>"].join("")
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
    }

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
        lang = lang.replace(/_/g, "+")
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

              // top repositories
              $("#tt_repositories").show();
              var sortable = [];
              for (var r in d["repositories"]) {
                sortable.push([r, d["repositories"][r]]);
              }
              sortable = sortable.sort(function(a, b) {return b[1] - a[1]}).slice(0, 3);

              $("#tt_repositories_value").text($.map(sortable, function(o) {
                var re = /^[^\/]+\//
                return o[0].replace(re, "");
              }).join(", "));
            } else {
              $("#tt_contributors").hide();
              $("#tt_repositories").hide();
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