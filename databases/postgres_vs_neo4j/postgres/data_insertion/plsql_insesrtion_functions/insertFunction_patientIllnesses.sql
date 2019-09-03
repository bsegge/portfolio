CREATE OR REPLACE FUNCTION add_patient_illness(pat_id int
                                              , ill_id int)
    RETURNS boolean AS
$$
DECLARE
    inserted_patient boolean := false;
    p_id             int;
    i_id             int;
BEGIN

    SELECT people_id
    INTO p_id
    FROM people p
    WHERE p.people_id = pat_id;

    SELECT illness_id
    INTO i_id
    FROM illnesses i
    WHERE i.illness_id = ill_id;

    INSERT INTO patients_illnesses
    VALUES (DEFAULT, p_id, i_id);

    inserted_patient := true;

    RETURN inserted_patient;
END;
$$ LANGUAGE plpgsql;
