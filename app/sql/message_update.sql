UPDATE message
SET
    text = @text@,
    title = @title@,
    attach = @attach@
WHERE id = @id@
