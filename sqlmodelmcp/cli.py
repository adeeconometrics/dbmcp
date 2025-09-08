import typer
from db import init_db, get_session
from generators import (generate_users,
                        generate_products,
                        generate_orders,
                        generate_order_items)

app = typer.Typer(help="MCP Demo Data Seeder CLI")


@app.command()
def seed(
    users: int = typer.Option(5, help="Number of users to generate"),
    products: int = typer.Option(10, help="Number of products to generate"),
    orders: int = typer.Option(8, help="Number of orders to generate"),
    items: int = typer.Option(20, help="Number of order items to generate"),
) -> None:
    """
    Generate fake data and insert into the database.
    """
    init_db()
    with next(get_session()) as session:
        # Generate users and products
        user_objs = generate_users(users)
        product_objs = generate_products(products)

        session.add_all(user_objs + product_objs)
        session.commit()

        # Refresh to get IDs
        user_ids = [u.user_id for u in session.exec(type(user_objs[0])).all()]
        product_ids = [p.product_id for p in session.exec(
            type(product_objs[0])).all()]

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
