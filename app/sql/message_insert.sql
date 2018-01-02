INSERT
INTO message (
    "id", "id_parent", "title", "time", "text",
    "author", "category", "allow", "attach", "ip"
)
VALUES (
    @id@, @id_parent@, @title@, @time@, @text@,
    @author@, @category@, @allow@, @attach@, @ip@
)
