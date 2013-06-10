.headers on
.mode csv

-- Gets the unique list of locations
-- for all actors who performed one of the "contribution"
-- event types for any of the top 50 C# repos
SELECT DISTINCT(actor_attributes_location) AS location
FROM event
WHERE
  type IN (
    'IssuesEvent',
    'PublicEvent',
    'PullRequestEvent',
    'PushEvent'
  )
  AND repository_url IN (
    'https://github.com/mono/MonoGame',
    'https://github.com/SignalR/SignalR',
    'https://github.com/mono/mono',
    'https://github.com/monospider/monogame',
    'https://github.com/ServiceStack/ServiceStack',
    'https://github.com/gmy77/d3sharp',
    'https://github.com/jagregory/fluent-nhibernate',
    'https://github.com/restsharp/RestSharp',
    'https://github.com/ravendb/ravendb',
    'https://github.com/NancyFx/Nancy',
    'https://github.com/hbons/SparkleShare',
    'https://github.com/gitextensions/gitextensions',
    'https://github.com/pubnub/pubnub-api',
    'https://github.com/AutoMapper/AutoMapper',
    'https://github.com/mono/monodevelop',
    'https://github.com/xamarin/monodroid-samples',
    'https://github.com/nhibernate/nhibernate-core',
    'https://github.com/Redth/PushSharp',
    'https://github.com/ServiceStack/ServiceStack.Text',
    'https://github.com/SamSaffron/dapper-dot-net',
    'https://github.com/DotNetOpenAuth/DotNetOpenAuth',
    'https://github.com/robconery/massive',
    'https://github.com/ligershark/webdevchecklist.com',
    'https://github.com/schambers/fluentmigrator',
    'https://github.com/mongodb/mongo-csharp-driver',
    'https://github.com/subsonic/SubSonic-3.0',
    'https://github.com/xamarin/mobile-samples',
    'https://github.com/SamSaffron/MiniProfiler',
    'https://github.com/NServiceBus/NServiceBus',
    'https://github.com/MahApps/MahApps.Metro',
    'https://github.com/ninject/ninject',
    'https://github.com/phatboyg/MassTransit',
    'https://github.com/facebook-csharp-sdk/facebook-csharp-sdk',
    'https://github.com/DarthFubuMVC/fubumvc',
    'https://github.com/xamarin/monotouch-samples',
    'https://github.com/toptensoftware/PetaPoco',
    'https://github.com/ServiceStack/ServiceStack.Redis',
    'https://github.com/migueldeicaza/MonoTouch.Dialog',
    'https://github.com/mausch/SolrNet',
    'https://github.com/joliver/EventStore',
    'https://github.com/koush/sqlite-net',
    'https://github.com/icsharpcode/ILSpy',
    'https://github.com/ServiceStack/ServiceStack.OrmLite',
    'https://github.com/chrisforbes/OpenRA',
    'https://github.com/machine/machine.specifications',
    'https://github.com/dotless/dotless',
    'https://github.com/Jessecar96/SteamBot',
    'https://github.com/mono/monotouch-bindings',
    'https://github.com/markrendle/Simple.Data',
    'https://github.com/JamesNK/Newtonsoft.Json'
  )
ORDER BY location;
