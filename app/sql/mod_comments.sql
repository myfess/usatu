SELECT {cols}
FROM message m
WHERE
    NOT EXISTS (SELECT 1 FROM comments_mod c WHERE c.comment_id = m.id)
    AND m.id_parent != 0
    AND m.allow != 'forum'
{orderby}
