import typer
from db import init_db, get_session
from seed.users import generate_user
from seed.products import generate_product
from seed.orders import generate_order
from seed.order_items import generate_order_item

app = typer.Typer(help="MCP Demo Data Seeder CLI")


@app.command()
def seed(
    users: int = typer.Option(5, help="Number of users to generate"),
    products: int = typer.Option(10, help="Number of products to generate"),
    orders: int = typer.Option(8, help="Number of orders to generate"),
    items: int = typer.Option(20, help="Number of order items to generate"),
):
    """
    Generate fake data and insert into the database.
    """
    init_db()
    with next(get_session()) as session:
        # Generate users and products
        user_objs = generate_user(users)
        product_objs = generate_product(products)

        session.add_all(user_objs + product_objs)
        session.commit()

        # Refresh to get IDs
        user_ids = [u.user_id for u in session.query(type(user_objs[0])).all()]
        product_ids = [p.product_id for p in session.query(
            type(product_objs[0])).all()]

        # Generate orders
        order_objs = generate_order(orders, user_ids)
        session.add_all(order_objs)
        session.commit()

        order_ids = [o.order_id for o in session.query(
            type(order_objs[0])).all()]

        # Generate order items
        item_objs = generate_order_item(items, order_ids, product_ids)
        session.add_all(item_objs)
        session.commit()

        typer.echo(
            f"✅ Seed complete: {users} users, {products} products, {orders} orders, {items} items"
        )


if __name__ == "__main__":
    app()
