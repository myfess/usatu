SELECT
    (
        SELECT subject
        FROM files_subjects
        WHERE id = @sid@
    ) AS subject,

    (
        SELECT type
        FROM files_types
        WHERE id = @tid@
    ) AS type
