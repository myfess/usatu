INSERT
INTO members_restore_pass (member_id, secret, dt)
VALUES (@member_id@, @secret@, NOW() at time zone 'UTC')
