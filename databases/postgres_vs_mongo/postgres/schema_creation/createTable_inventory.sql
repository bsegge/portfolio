CREATE TABLE inventory
(
    inv_id      SERIAL PRIMARY KEY,
    name        varchar(25),
    description varchar(255),
    quantity    int CHECK (quantity > 0)
);
