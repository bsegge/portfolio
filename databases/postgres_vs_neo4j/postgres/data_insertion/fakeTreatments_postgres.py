from faker import Faker

fake = Faker()

with open("fakeTreatments_postgres.sql", "w") as f:
    for i in range(750):
        f.write(
            f"INSERT INTO treatments VALUES(DEFAULT"
            f", 'treatment_name_{i}');\n"
        )
