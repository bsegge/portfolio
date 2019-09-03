from faker import Faker

fake = Faker()

with open("fake_users_mongo.txt", "w") as f:
    for i in range(1000):
        f.write(
            f'db.users.insert({{"email": "{fake.email()}"'
            f', "first_name":"{fake.first_name()}"'
            f', "last_name":"{fake.last_name()}"'
            f', "phone_number":"{fake.phone_number()}"'
            f', "address_01":"{fake.street_address()}"'
            f', "address_02":"{fake.secondary_address()}"'
            f', "city":"{fake.city()}"'
            f', "state":"{fake.state()}"'
            f', "zip":"{fake.zipcode()}"}})\n'
        )
