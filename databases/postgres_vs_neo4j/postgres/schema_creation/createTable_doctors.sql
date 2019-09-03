CREATE TABLE doctors
(
    doctor_id SERIAL PRIMARY KEY,
    people_id int REFERENCES people,
    unique (people_id)
);
