SELECT
    id,
    id_parent,
    title,
    text,
    (attach = 'yes') AS attach,
    (draft IS TRUE) AS draft,
    (
        SELECT count(*) > 0
        FROM blog
        WHERE message_id = @id@
    ) AS is_blog_post
FROM message
WHERE id = @id@
