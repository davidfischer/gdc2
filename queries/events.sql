.headers on
.mode csv


-- Gets the "contribution" events
-- for any of the top 200 repos
SELECT "type",
  repository_language,
  repository_url,
  actor_attributes_login,
  actor_attributes_type,
  actor_attributes_gravatar_id,
  actor_attributes_location
FROM event
WHERE
  type IN (
    'IssuesEvent',
    'PublicEvent',
    'PullRequestEvent',
    'PushEvent'
  )
  AND repository_name IN (
    SELECT DISTINCT(repository_name)
    FROM event
    WHERE repository_fork = 0
    ORDER BY repository_forks
    DESC LIMIT 200
  )
  AND repository_fork = 0
  AND "type" IS NOT NULL
  AND repository_language IS NOT NULL
  AND repository_url IS NOT NULL
  AND actor_attributes_login IS NOT NULL
  AND actor_attributes_location IS NOT NULL;
