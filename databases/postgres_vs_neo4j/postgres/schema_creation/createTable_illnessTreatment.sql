CREATE TABLE illness_treatment
(
    illness_treatment_id SERIAL PRIMARY KEY,
    illness_id           int REFERENCES illnesses,
    treatment_id         int REFERENCES treatments,
    unique (illness_id, treatment_id)
);
