SELECT
    t.*,
    c.name AS chair
FROM teachers t
LEFT JOIN chairs c ON (c.id = t.id_chair)
WHERE allow != 'yes'
ORDER BY id DESC
LIMIT 10
