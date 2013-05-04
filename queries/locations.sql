.headers on
.mode csv

-- Gets the unique list of locations
-- for all actors who performed one of the "contribution"
-- event types for any of the top 200 repos
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
    SELECT DISTINCT(repository_url)
    FROM event
    WHERE repository_fork = 0
    ORDER BY repository_forks
    DESC LIMIT 200
  )
ORDER BY location;
