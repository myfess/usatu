SELECT value
FROM cache
WHERE
    method = @method@
    AND params = @params@
    AND (NOW() at time zone 'UTC' - date_time) < interval '{CACHE_INTERVAL}'
ORDER BY id DESC
LIMIT 1
