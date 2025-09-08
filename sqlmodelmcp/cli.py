from sqlmodel import select
import typer


from db import init_db, get_session
from generators import (generate_addresses,
                        generate_categories,
                        generate_users,
                        generate_products,
                        generate_orders,
                        generate_order_items)
from dataenums import Categiories

app = typer.Typer(help="MCP Demo Data Seeder CLI")


@app.command()
def seed(
    users: int = typer.Option(5, help="Number of users to generate"),
    products: int = typer.Option(10, help="Number of products to generate"),
    orders: int = typer.Option(8, help="Number of orders to generate"),
    items: int = typer.Option(20, help="Number of order items to generate"),
    addresses: int = typer.Option(10, help="Number of addresses to generate"),
) -> None:
    """
    Generate fake data and insert into the database.
    """
    init_db()
    with next(get_session()) as session:
        # 1. Generate and insert categories
        category_objs = generate_categories()
        session.add_all(category_objs)
        session.commit()

        # 2. Cache category name to id mapping
        categories_in_db = session.exec(select(type(category_objs[0]))).all()
        category_id_map = {c.name: c.category_id for c in categories_in_db}

        # 3. Generate addresses, users, products
        address_objs = generate_addresses(addresses)
        session.add_all(address_objs)
        session.commit()
        address_ids = [a.address_id for a in session.exec(
            select(type(address_objs[0]))).all()]

        user_objs = generate_users(users, address_ids)
        product_objs = generate_products(products, category_id_map)
        session.add_all(user_objs + product_objs)
        session.commit()

        # Refresh to get IDs

        user_ids = [u.user_id for u in session.exec(
            select(type(user_objs[0]))).all()]
        product_ids = [p.product_id for p in session.exec(
            select(type(product_objs[0]))).all()]

        # Generate orders
        order_objs = generate_orders(orders, user_ids)
        session.add_all(order_objs)
        session.commit()

        order_ids = [o.order_id for o in session.query(
            type(order_objs[0])).all()]

        # Generate order items
        item_objs = generate_order_items(items, order_ids, product_ids)
        session.add_all(item_objs)
        session.commit()

        typer.echo(
            f"✅ Seed complete: {users} users, {products} products, {orders} orders, {items} items"
        )


if __name__ == "__main__":
    app()
