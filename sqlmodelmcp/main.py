from db import init_db, get_session
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem


def seed_data():
    init_db()
    with next(get_session()) as session:
        # Create a user
        user = User(name="Alice", email="alice@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create a product
        product = Product(name="Laptop", price=1200.0, stock_quantity=10)
        session.add(product)
        session.commit()
        session.refresh(product)

        # Create an order
        order = Order(user_id=user.user_id)
        session.add(order)
        session.commit()
        session.refresh(order)

        # Add order item
        order_item = OrderItem(order_id=order.order_id,
                               product_id=product.product_id, quantity=2)
        session.add(order_item)
        session.commit()

        print(f"User {user.name} ordered {order_item.quantity} x {product.name}")


if __name__ == "__main__":
    seed_data()
