WITH RECURSIVE
    t AS (
        SELECT
            *, 1 AS level
        FROM "struct_message"
        WHERE id = @id@

        UNION

        SELECT
            sm.*, (t.level + 1) AS level
        FROM t
        INNER JOIN "struct_message" sm ON (sm.id = t.id_parent)
    )

SELECT "EN" AS en, "RU" AS ru
FROM t
ORDER BY level DESC
LIMIT 1
