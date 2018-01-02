SELECT *
FROM message
WHERE
    id_parent = @p_id@
    AND time < @time@
