CREATE OR REPLACE FUNCTION add_order(f_name varchar(50),
                                     l_name varchar(50),
                                     recipe varchar(50))
    RETURNS boolean AS
$$
DECLARE
    inserted_user  boolean := false;
    u_id           int;
    r_id           int;
    inventory_item varchar(50);
BEGIN

    SELECT user_id
    INTO u_id
    FROM users u
    WHERE u.first_name = f_name
      AND u.last_name = l_name;

    SELECT recipe_id
    INTO r_id
    FROM recipes r
    WHERE r.name ILIKE recipe;

    UPDATE inventory
    SET quantity = quantity - ingredients.units
    FROM ingredients
    WHERE inv_id = ingredients.inventory_id
      AND ingredients.recipe_id = r_id;

    IF u_id IS NULL THEN
        INSERT INTO users (user_id, first_name, last_name)
        VALUES (DEFAULT, f_name, l_name) RETURNING user_id INTO u_id;

        inserted_user := true;
    END IF;

    INSERT INTO orders (user_id, time_placed, recipe_id)
    VALUES (u_id, DEFAULT, r_id);

    RETURN inserted_user;
END;
$$ LANGUAGE plpgsql;
