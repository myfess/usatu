SELECT *
FROM message
WHERE
    allow = 'no'
    AND id_parent = 0
ORDER BY id DESC
LIMIT 10
