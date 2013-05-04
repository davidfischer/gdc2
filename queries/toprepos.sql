.headers on
.mode csv

-- Gets the top 200 repos by number of forks
SELECT DISTINCT(repository_url)
FROM event
WHERE repository_fork = 0
ORDER BY repository_forks
DESC LIMIT 200;
