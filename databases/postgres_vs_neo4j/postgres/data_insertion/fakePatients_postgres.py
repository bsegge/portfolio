# adds our regular patients to the patients_doctors table
# as well as the patients_illnesses table

from faker import Faker
import random

fake = Faker()

with open("fakePatients_postgres.sql", "w") as f:
    for i in range(1, 10001):
        rand_docs = random.sample(range(1, 100), random.randint(1, 5))
        for j in rand_docs:
            f.write(
                f"SELECT add_patient_doctors('{i}'"
                f", '{j}');\n"
            )
        rand_illness = random.sample(range(1, 1001), random.randint(1, 3))
        for j in rand_illness:
            f.write(
                f"SELECT add_patient_illness('{i}'"
                f", '{j}');\n"
            )
