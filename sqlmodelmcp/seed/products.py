from faker import Faker
from typing import List
from models.product import Product
import random

fake = Faker()


def generate_product(n: int) -> List[Product]:
    products = []
    for _ in range(n):
        product = Product(
            name=fake.word().capitalize(),
            price=round(random.uniform(10.0, 2000.0), 2),
            stock_quantity=random.randint(0, 100)
        )
        products.append(product)
    return products
