UPDATE message
SET allow = 'yes'
WHERE id = @id@;

INSERT
INTO comments_mod(comment_id)
VALUES(@id@);
