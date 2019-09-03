from faker import Faker

fake = Faker()

with open("fake_users_postgres.sql", "w") as f:
    for i in range(1000):
        f.write(
            f"INSERT INTO users VALUES(DEFAULT, '{fake.email()}'"
            f", '{fake.first_name()}'"
            f", '{fake.last_name()}'"
            f", '{fake.phone_number()}'"
            f", '{fake.street_address()}'"
            f", '{fake.secondary_address()}'"
            f", '{fake.city()}'"
            f", '{fake.state()}'"
            f", '{fake.zipcode()}');\n"
        )
