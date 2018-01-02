SELECT
    id,
    id_parent,
    title,
    text,
    (attach = 'yes') AS attach
FROM message
WHERE id = @id@
