UPDATE members
SET password = @password@
WHERE id = @mid@
RETURNING id, name, email
