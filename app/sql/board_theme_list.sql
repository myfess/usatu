SELECT
    *,
    (
        SELECT count(*)
        FROM message
        WHERE id_parent = bt.id
    ) cnt
FROM board_theme bt
ORDER BY dt_last_msg DESC
LIMIT 40
