INSERT
INTO "id"
    SELECT
        coalesce(MAX("id"."id") + 1, 1)
    FROM "id"
RETURNING "id"
