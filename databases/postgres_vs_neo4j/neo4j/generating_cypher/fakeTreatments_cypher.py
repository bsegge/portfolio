# adds treatment nodes and relationships to illneses

from faker import Faker
import random

fake = Faker()

with open("fakeTreatments_cypher.txt", "w") as f:
    for i in range(1, 751):
        fake_treatment = f"treatment_{i}"
        f.write(
            f"CREATE (t:Treatment {{name: '{fake_treatment}'}})\n"
            f"With 1 as dummy\n"
        )
    for j in range(1, 1001):
        for k in range(random.randint(1, 3)):
            f.write(
                f"MATCH (i:Illness{{name: 'illness_{j}'}}),\n"
                f"(t:Treatment {{name: 'treatment_{random.randint(1, 751)}'}})\n"
                f"CREATE (i)<-[:treats]-(t)\n"
                f"With 1 as dummy\n"
            )
