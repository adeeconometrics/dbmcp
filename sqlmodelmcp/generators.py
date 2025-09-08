from typing import List
from random import uniform, randint
from faker import Faker
from models import User, Product, Order, OrderItem, OrderStatus


fake = Faker()


def generate_users(n: int) -> List[User]:
    """Generate a list of User instances."""
    return [
        User(
            name=fake.name(),
            email=fake.unique.email()
        ) for _ in range(n)
    ]


def generate_products(n: int) -> List[Product]:
    """Generate a list of Product instances."""
    return [
        Product(
            name=fake.word().capitalize(),
            price=round(uniform(10.0, 2500.0), 2),
            stock_quantity=randint(0, 100)
        ) for _ in range(n)
    ]


def generate_orders(n: int, user_ids: List[int]) -> List[Order]:
    """Generate a list of Order instances."""
    return [
        Order(
            user_id=fake.random_element(elements=user_ids),
            order_date=fake.date_time_this_year(),
            status=str(fake.random_element(elements=list(OrderStatus)))
        ) for _ in range(n)
    ]


def generate_order_items(n: int, order_ids: List[int], product_ids: List[int]) -> List[OrderItem]:
    """Generate a list of OrderItem instances."""
    return [
        OrderItem(
            order_id=fake.random_element(elements=order_ids),
            product_id=fake.random_element(elements=product_ids),
            quantity=randint(1, 10)
        ) for _ in range(n)
    ]
