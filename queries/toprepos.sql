.headers on
.mode csv

-- Gets the top 200 repos by number of forks
SELECT repository_url, MAX(repository_forks) AS forks
FROM event
WHERE repository_fork = 0
  -- Some URLs are in the database with the username
  -- incorrectly stripped
  AND repository_url NOT LIKE 'https://github.com//%'
GROUP BY repository_url
ORDER BY forks DESC
LIMIT 200;
