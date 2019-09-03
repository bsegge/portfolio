# adds our doctors who are patients to the patients_doctors table
# as well as the patients_illnesses table

from faker import Faker
import random

fake = Faker()

rand_doc_patients = random.sample(range(10000, 10100), 35)

with open("fakePatientsDoctors_postgres.sql", "w") as f:
    for i in rand_doc_patients:
        rand_docs = random.sample(range(1, 100), random.randint(1, 5))
        for j in rand_docs:
            f.write(
                f"SELECT add_patient_doctors('{i}'"
                f", '{j}');\n"

            )
    for i in rand_doc_patients:
        rand_illness = random.sample(range(1, 1000), random.randint(1, 3))
        for j in rand_illness:
            f.write(
                f"SELECT add_patient_illness('{i}'"
                f", '{j}');\n"
            )
