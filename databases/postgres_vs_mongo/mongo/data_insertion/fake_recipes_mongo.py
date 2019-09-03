from faker import Faker

fake = Faker()

with open("fake_recipes_mongo.txt", "w") as f:
    for i in range(25):
        f.write(
            f'db.recipes.insert({{"name": "recipe_name_{i}"'
            f', "description": "recipe_description_{i}"'
            f', "instructions":"recipe_instruction_{i}"'
            f', "ingredients": [{{"name": "ing_{i}", "qty": 1}}, {{"name": "ing_{i + 1}", "qty": 2}}]}})\n'
        )
