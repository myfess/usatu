SELECT
    t.*,
    c.name AS chair_name,
    c.short_name AS chair_short_name,
    f.short_name AS fc_short_name
FROM teachers AS t
LEFT JOIN chairs AS c ON (c.id = t.id_chair)
LEFT JOIN chairs AS f ON (f.id = c.id_parent)
WHERE
    t.id = @tid@
