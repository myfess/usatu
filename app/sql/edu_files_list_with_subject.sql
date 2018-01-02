SELECT
    files.id,
    files.ext,
    files.description,
    files_types.type,
    files.size,
    files.time,
    files.author
FROM files
LEFT JOIN files_types ON (files_types.id = files.type::int)
WHERE
    files.allow = 'yes'
    AND files.subject = (@subject@)::text
    {cond}
ORDER BY files.time DESC
