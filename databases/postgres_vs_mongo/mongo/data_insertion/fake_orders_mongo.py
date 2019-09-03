from faker import Faker

fake = Faker()

import random

with open("fake_orders_mongo.txt", "w") as f:
    for i in range(50000):
        f.write(
            f"add_order('{fake.first_name()}'"
            f", '{fake.last_name()}'"
            f", 'recipe_name_{random.randint(0, 24)}')\n"
        )
