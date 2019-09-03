from faker import Faker

fake = Faker()

with open("fakePeople_postgres.sql", "w") as f:
    for i in range(10100):
        f.write(
            f"INSERT INTO people VALUES(DEFAULT, '{fake.email()}'"
            f", '{fake.first_name()}'"
            f", '{fake.last_name()}'"
            f", '{fake.phone_number()}'"
            f", '{fake.street_address()}'"
            f", '{fake.secondary_address()}'"
            f", '{fake.city()}'"
            f", '{fake.state()}'"
            f", '{fake.zipcode()}');\n"
        )
