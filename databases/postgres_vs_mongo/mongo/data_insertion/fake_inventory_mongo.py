from faker import Faker

fake = Faker()

with open("fake_inventory_mongo.txt", "w") as f:
    for i in range(0, 27):
        f.write(
            f'db.inventory.insert({{"name": "ing_{i}"'
            f', "description": "ingredient_description_{i}"'
            f', "quantity":500000}})\n'
        )
