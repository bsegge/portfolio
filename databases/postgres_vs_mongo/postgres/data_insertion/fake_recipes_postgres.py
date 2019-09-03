from faker import Faker

fake = Faker()

with open("fake_recipes_postgres.sql", "w") as f:
    for i in range(25):
        f.write(
            f"INSERT INTO recipes VALUES(DEFAULT"
            f", 'recipe_name_{i}'"
            f", 'recipe_description_{i}'"
            f", 'recipe_instruction_{i}');\n"
        )
