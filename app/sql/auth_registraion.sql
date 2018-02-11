INSERT
INTO members (id, name, password, email)
VALUES (
    (SELECT max(m.id) + 1 FROM members m),
    @name@, @password@, @email@
)
RETURNING id, name, email
