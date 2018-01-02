UPDATE teachers
SET
    name = @name@,
    id_chair = @id_chair@,
    subject = @subject@,
    information = @information@,
    fotos = @fotos@
WHERE id = @id@
