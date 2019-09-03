CREATE TABLE patients_illnesses
(
    pi_id      SERIAL PRIMARY KEY,
    people_id  int REFERENCES people,
    illness_id int REFERENCES illnesses,
    unique (people_id, illness_id)
);
