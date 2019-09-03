import random

with open('fake_ingredients_postgres.sql', 'w') as f:
    for i in range(1, 7):
        for recipe_num in range(1, 26):
            inventory_id = i
            recipe_id = recipe_num
            units = random.randint(1, 3)
            f.write(
                f'INSERT INTO ingredients VALUES({inventory_id}, {recipe_id}, {units});\n'
            )
