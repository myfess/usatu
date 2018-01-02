SELECT
    f.type AS id,
    ft.type
FROM files f
LEFT JOIN files_types ft ON (ft.id = f.type::int)
WHERE
    f.subject = (@subject@)::text
    AND f.allow = 'yes'
GROUP BY f.type, ft.type
ORDER BY ft.type
