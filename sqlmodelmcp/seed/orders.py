from faker import Faker
from typing import List
from models.order import Order, OrderStatus
from random import choice
from datetime import datetime

fake = Faker()


def generate_order(n: int, user_ids: List[int]) -> List[Order]:
    """Generate orders tied to existing users."""
    orders = []
    for _ in range(n):
        order = Order(
            user_id=choice(user_ids),
            order_date=fake.date_time_between(
                start_date="-1y", end_date="now"),
            status=choice([
                OrderStatus.PENDING,
                OrderStatus.SHIPPED,
                OrderStatus.DELIVERED,
                OrderStatus.CANCELLED,
            ]),
        )
        orders.append(order)
    return orders
