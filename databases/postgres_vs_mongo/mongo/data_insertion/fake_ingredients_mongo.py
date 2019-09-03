import random

with open('fake_ingredients_mongo.txt', 'w') as f:
    for i in range (1,7):
        for recipe_num in range(1,26):
            inventory_id = i
            recipe_id = recipe_num
            units = random.randint(1,3)
            f.write(
            f'db.ingredients.insert({{"inventory_id": {inventory_id}'
            f', "recipe_id": {recipe_id}'
            f', "units":{units}}})\n'
            )
