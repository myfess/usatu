SELECT
    ft.id,
    ft.type
FROM files_types ft
WHERE
    EXISTS (
        SELECT 1
        FROM files
        WHERE
        files.type = ft.id::text
        AND files.allow = 'yes'
    )
ORDER BY ft.type ASC
