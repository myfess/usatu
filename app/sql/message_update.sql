UPDATE message
SET
    text = @text@,
    title = @title@,
    attach = @attach@,
    draft = @draft@
WHERE id = @id@
