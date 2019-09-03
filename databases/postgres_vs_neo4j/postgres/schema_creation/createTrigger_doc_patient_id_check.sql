CREATE OR REPLACE FUNCTION id_check() RETURNS trigger AS
$$
DECLARE
    doc_people_id int;
BEGIN
    SELECT doctors.people_id
    into doc_people_id
    FROM doctors
    WHERE doctors.doctor_id = NEW.doctor_id;

    IF doc_people_id = NEW.people_id THEN
        RAISE EXCEPTION 'A doctor cannot be a patient of himself!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER check_id
    BEFORE INSERT
    ON patients_doctors
    FOR EACH ROW
EXECUTE PROCEDURE id_check();
