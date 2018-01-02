SELECT
    cookie_id.login,
    u.permission,
    m.id,
    m.avatar
FROM cookie_id
LEFT JOIN users u ON (u.login = cookie_id.login)
LEFT JOIN members m ON (m.name = cookie_id.login)
WHERE cookie_id.id = @cookie_id@
