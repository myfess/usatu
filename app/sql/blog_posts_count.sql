SELECT count(*)
FROM blog b
INNER JOIN message m ON (m.id = b.message_id)
WHERE
    m.allow = 'yes'
    AND
    (
        draft IS NOT TRUE
        OR
        author = @username@
    )
