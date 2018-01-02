SELECT count(*)
FROM message
WHERE
    id_parent = 0
    AND allow = 'yes'
    AND category = ANY(ARRAY[{cats}])
