from faker import Faker

fake = Faker()

with open("fakeIllnesses_postgres.sql", "w") as f:
    for i in range(1000):
        f.write(
            f"INSERT INTO illnesses VALUES(DEFAULT"
            f", 'illness_name_{i}');\n"
        )
