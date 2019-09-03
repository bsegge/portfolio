# adds illness nodes

from faker import Faker
import random

fake = Faker()

with open("fakeIllnesses_cypher.txt", "w") as f:
    for i in range(1, 1001):
        f.write(
            f"CREATE (i:Illness {{name: 'illness_{i}'}})\n"
            f"With 1 as dummy\n"
        )
