SELECT
    (
        SELECT count(*)
        FROM message
        WHERE
            id_parent = @pid@
            AND "time" < (
                SELECT m."time"
                FROM message m
                WHERE m.id = @cid@
            )
    ) AS _count,

    (
        SELECT count(*) > 0
        FROM message
        WHERE id = @pid@
    ) AS news,

    (
        SELECT user_id
        FROM foto
        WHERE id = @pid@
    ) AS photos_user_id,

    (
        SELECT count(*) > 0
        FROM teachers
        WHERE id = @pid@
    ) AS teachers
