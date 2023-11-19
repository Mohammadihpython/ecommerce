from faker import Faker
fake = Faker('fa_IR')
for _ in range(10):
    print(fake.phone_number())