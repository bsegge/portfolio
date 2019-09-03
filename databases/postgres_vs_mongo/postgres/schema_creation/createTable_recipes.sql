CREATE TABLE recipes
(
    recipe_id    SERIAL PRIMARY KEY,
    name         varchar(25),
    description  varchar(255),
    instructions text
);
