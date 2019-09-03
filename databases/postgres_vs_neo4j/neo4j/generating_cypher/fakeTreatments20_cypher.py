## used for testing, feel free to ignore

from faker import Faker
import random

fake = Faker()

with open("fakeTreatments20_cypher.txt", "w") as f:
    for i in range(1, 21):
        fake_treatment = f"treatment_{i}"
        f.write(
            f"CREATE (t:Treatment {{name: '{fake_treatment}'}})\n"
            f"With 1 as dummy\n"
        )
    for j in range(1, 11):
        for k in range(random.randint(1, 3)):
            f.write(
                f"MATCH (i:Illness{{name: 'illness_{j}'}}),\n"
                f"(t:Treatment {{name: 'treatment_{random.randint(1, 20)}'}})\n"
                f"CREATE (i)<-[:treats]-(t)\n"
                f"With 1 as dummy\n"
            )
