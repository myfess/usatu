INSERT
INTO files_types (type)
VALUES (@type@)
RETURNING "id"
