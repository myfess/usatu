UPDATE board_theme
SET title = @title@
WHERE
    id = (
        SELECT id_parent
        FROM message
        WHERE id = @id@
    )
