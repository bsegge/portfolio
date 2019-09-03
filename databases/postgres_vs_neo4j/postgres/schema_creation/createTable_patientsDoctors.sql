CREATE TABLE patients_doctors
(
    pd_id     SERIAL PRIMARY KEY,
    people_id int REFERENCES people,
    doctor_id int REFERENCES doctors,
    unique (people_id, doctor_id)
);
