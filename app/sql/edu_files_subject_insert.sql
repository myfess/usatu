INSERT
INTO files_subjects (subject)
VALUES (@subject@)
RETURNING "id"
