## used for testing, feel free to ignore

# adds our patients to the patients nodes
# first 35 are also doctors
# also adds the remaining doctors
# creates patient-illness and patient-doctor relationships

from faker import Faker
import random

fake = Faker()

with open("fakePatients20_cypher.txt", "w") as f:
    # inserting patients (including 35 patient-doctors)
    for i in range(1, 21):
        fake_pat = fake.name()
        if i < 7:
            f.write(
                f"CREATE (p:Patient:Doctor {{name: '{fake_pat}', id:{i}}})\n"
                f"With 1 as dummy\n"
            )
        else:
            f.write(
                f"CREATE (p:Patient {{name: '{fake_pat}', id:{i}}})\n"
                f"With 1 as dummy\n"
            )

        # creating illness relationships
        rand_illness = random.sample(range(1, 11), random.randint(1, 3))
        for j in rand_illness:
            f.write(
                f"MATCH (p:Patient{{name: '{fake_pat}'}}),\n"
                f"(i:Illness {{name: 'illness_{j}'}})\n"
                f"CREATE (p)-[h:has_illness]->(i)\n"
                f"With 1 as dummy\n"
            )

    # inserting remaining doctors
    for d in range(21, 32):
        fake_doc = fake.name()
        f.write(
            f"CREATE (d:Doctor {{name: '{fake_doc}', id:{d}}})\n"
            f"With 1 as dummy\n"
        )

    # creating patient-doctor relationships
    for l in range(1, 21):
        for k in range(random.randint(1, 5)):
            rand_doc = random.choice([random.randint(1, 6), random.randint(21, 31)])
            if rand_doc != l:
                f.write(
                    f"MATCH (p:Patient{{id: {l}}}),\n"
                    f"(d:Doctor {{id: {rand_doc}}})\n"
                    f"CREATE (p)-[:doctored_by]->(d)\n"
                    f"With 1 as dummy\n"
                )
