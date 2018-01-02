WITH
    t AS (
        INSERT
        INTO cache (method, params, value, date_time)
        VALUES (@method@, @params@, @value@, NOW() at time zone 'UTC')
        RETURNING id
    )

DELETE
FROM cache
WHERE
    id != (SELECT t.id FROM t)
    AND method = @method@
    AND params = @params@
