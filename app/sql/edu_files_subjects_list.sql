SELECT
    fs.id,
    fs.subject,
    count(*) AS _count
FROM files f
LEFT JOIN files_subjects fs ON (fs.id = f.subject::int)
WHERE
    f.allow = 'yes'
GROUP BY fs.id, fs.subject
ORDER BY subject
