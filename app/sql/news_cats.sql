WITH RECURSIVE
    t AS (
        SELECT
            id, id_parent
        FROM "struct_message"
        WHERE "EN" = @name@

        UNION

        SELECT
            sm.id, sm.id_parent
        FROM t
        INNER JOIN "struct_message" sm ON (sm.id_parent = t.id)
    )

SELECT array_agg(id::text)
FROM t
