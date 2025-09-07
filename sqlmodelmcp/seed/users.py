from faker import Faker
from typing import List
from models.user import User

fake = Faker()


def generate_user(n: int) -> List[User]:
    users = []
    for _ in range(n):
        user = User(
            name=fake.name(),
            email=fake.unique.email()
        )
        users.append(user)
    return users
