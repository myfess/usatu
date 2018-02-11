SELECT
    b.id AS blog_post_id,
    m.*
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
ORDER BY
    attach = 'yes' DESC,
    time DESC
LIMIT @count@
OFFSET @start@
