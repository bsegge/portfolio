SET timezone = 'America/Denver';

CREATE TABLE orders
(
    user_id     int REFERENCES users,
    time_placed timestamp DEFAULT now(),
    recipe_id   int REFERENCES recipes
);
