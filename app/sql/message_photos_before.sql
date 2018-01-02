SELECT count(*)
FROM foto
WHERE
    user_id = @user_id@
    AND id <= @id@
