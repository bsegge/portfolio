CREATE TABLE treatments
(
    treatment_id SERIAL PRIMARY KEY,
    name         varchar(100),
    unique (name)
);
