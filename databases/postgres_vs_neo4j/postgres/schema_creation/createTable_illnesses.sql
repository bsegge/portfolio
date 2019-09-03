CREATE TABLE illnesses
(
    illness_id SERIAL PRIMARY KEY,
    name       varchar(100),
    unique (name)
);
