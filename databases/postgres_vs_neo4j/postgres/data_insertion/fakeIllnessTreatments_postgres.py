from faker import Faker
import random

fake = Faker()

with open("fakeIllnessTreatment_postgres.sql", "w") as f:
    for i in range(1000):
        for j in range(random.randint(1, 3)):
            f.write(
                f"INSERT INTO illness_treatment VALUES (DEFAULT"
                f", '{i}'"
                f", '{random.randint(0, 750)}');\n"
            )
