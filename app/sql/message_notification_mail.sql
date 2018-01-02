SELECT
    m1.author AS new_author,
    m2.author AS old_author,
    m1.text AS new_text,
    m2.text AS old_text,
    m2.id AS old_id,
    m.email
FROM message m1
INNER JOIN message m2 ON (m2.id_parent != 0 AND m2.id = m1.id_parent)
LEFT JOIN members m ON (m.name = m2.author)
WHERE m1.id = @id@
