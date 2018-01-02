SELECT
    COALESCE(
        (
            SELECT title
            FROM board_theme
            WHERE id = @id@
        ),
        ''
    )
