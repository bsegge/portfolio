CREATE OR REPLACE FUNCTION add_patient_doctors(pat_id int
                                              , doc_id int)
    RETURNS boolean AS
$$
DECLARE
    inserted_patient boolean := false;
    d_id             int;
    p_id             int;
    i_id             int;
BEGIN

    SELECT doctor_id
    INTO d_id
    FROM doctors d
    WHERE d.doctor_id = doc_id;

    SELECT people_id
    INTO p_id
    FROM people p
    WHERE p.people_id = pat_id;

    INSERT INTO patients_doctors
    VALUES (DEFAULT, p_id, d_id);

    inserted_patient := true;

    RETURN inserted_patient;
END;
$$ LANGUAGE plpgsql;
