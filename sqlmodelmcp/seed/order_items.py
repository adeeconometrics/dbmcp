from typing import List
from models.order_item import OrderItem
from random import choice, randint


def generate_order_item(n: int, order_ids: List[int], product_ids: List[int]) -> List[OrderItem]:
    """Generate order items tied to existing orders and products."""
    items = []
    for _ in range(n):
        item = OrderItem(
            order_id=choice(order_ids),
            product_id=choice(product_ids),
            quantity=randint(1, 5),
        )
        items.append(item)
    return items
