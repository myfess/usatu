SELECT member_id
FROM members_restore_pass
WHERE
    secret = @secret@
    AND (NOW() at time zone 'UTC' - dt) < interval '1 day'
