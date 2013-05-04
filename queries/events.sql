.headers on
.mode csv


-- Gets the count of all "contribution" events
-- for any of the top 200 repos
SELECT COUNT(*)
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
  AND repository_fork = 0;
