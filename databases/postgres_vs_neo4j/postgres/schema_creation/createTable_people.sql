CREATE TABLE people
(
    people_id    SERIAL PRIMARY KEY,
    email        varchar(100),
    first_name   varchar(25),
    last_name    varchar(50),
    phone_number varchar(25),
    address_01   varchar(100),
    address_02   varchar(100),
    city         varchar(50),
    state        varchar(50),
    zip          varchar(5),
    unique (first_name, last_name, phone_number)
);
