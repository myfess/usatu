WITH RECURSIVE
    t AS (
        SELECT m.id
        FROM message m
        WHERE id_parent = @id@

        UNION

        SELECT m.id
        FROM t
        INNER JOIN message m ON (m.id_parent = t.id)
    )

SELECT count(*) FROM t
