CREATE TABLE ingredients
(
    inventory_id int REFERENCES inventory,
    recipe_id    int REFERENCES recipes,
    units        int
);
