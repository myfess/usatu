SELECT
    *
FROM message
WHERE
    id_parent = 0
    AND allow = 'yes'
    AND category = ANY(ARRAY[{cats}])
ORDER BY
    attach = 'yes' DESC,
    time DESC
LIMIT @count@
OFFSET @start@
