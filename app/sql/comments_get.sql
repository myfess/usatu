WITH RECURSIVE
    init AS (
        SELECT m.id
        FROM message m
        WHERE
            id_parent = @id_parent@
        ORDER BY m.time
        LIMIT @page_size@
        OFFSET @offset@
    ),

    t AS (
        SELECT
            m.*,
            0 AS level,
            array[id] AS path
        FROM message m
        WHERE id = ANY(ARRAY(SELECT * from init))

        UNION

        SELECT
            m.*,
            (t.level + 1) AS level,
            array_append(t.path, m.id)
        FROM t
        INNER JOIN message m ON (m.id_parent = t.id)
    )

SELECT
    t.*,
    m.avatar
FROM t
LEFT JOIN members m ON (m.name = t.author)
ORDER BY path
