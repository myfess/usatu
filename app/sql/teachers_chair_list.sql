SELECT
    id, name
FROM teachers
WHERE
    allow = 'yes'
    AND id_chair = @chair_id@
ORDER BY name
