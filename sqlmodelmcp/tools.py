from typing import Any, Dict, List, Optional
from sqlmodel import Session, select

from db import engine
from models import User, Product, Order, Category, OrderItem


def get_users(limit: int = 25) -> List[Dict[str, Any]]:
    """List users with optional limit.

    Args:
        limit (int, optional): Maximum number of users to return. Defaults to 25.

    Returns:
        List[Dict[str, Any]]: List of user dictionaries.
    """
    with Session(engine) as session:
        stmt = select(User).limit(max(1, limit))
        users = session.exec(stmt).all()
        return [
            {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "user_id": user.user_id,
            }
            for user in users
        ]


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID.

    Args:
        user_id (str): User ID to retrieve.

    Returns:
        Optional[Dict[str, Any]]: User dictionary if found, None otherwise.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return None
        return {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "user_id": user.user_id,
        }


def get_products(limit: int = 50) -> List[Dict[str, Any]]:
    """List products with optional limit.

    Args:
        limit (int, optional): Maximum number of products to return. Defaults to 50.

    Returns:
        List[Dict[str, Any]]: List of product dictionaries.
    """
    with Session(engine) as session:
        stmt = select(Product, Category).join(
            Category, Product.category_id == Category.category_id).limit(max(1, limit))
        results = session.exec(stmt).all()
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "price": float(product.price),
                "stock_quantity": int(product.stock_quantity),
                "category_name": category.name,
            }
            for product, category in results
        ]


def get_products_by_name(q: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Search for products by name with optional limit.

    Args:
        q (str): Search query string.
        limit (int, optional): Maximum number of products to return. Defaults to 25.

    Returns:
        List[Dict[str, Any]]: List of product dictionaries matching the search query.
    """
    with Session(engine) as session:
        stmt = select(Product).where(Product.name.ilike(f"%{q}%")).limit(
            max(1, limit)
        )
        prods = session.exec(stmt).all()
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "price": float(product.price),
                "stock_quantity": int(product.stock_quantity),
            }
            for product in prods
        ]


def get_orders(
    limit: int = 25, user_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List orders with optional limit and user filter.

    Args:
        limit (int, optional): Maximum number of orders to return. Defaults to 25.
        user_id (Optional[int], optional): User ID to filter orders by. Defaults to None.

    Returns:
        List[Dict[str, Any]]: List of order dictionaries.
    """
    with Session(engine) as session:
        stmt = select(Order)
        if user_id is not None:
            stmt = stmt.where(Order.user_id == user_id)
        stmt = stmt.limit(max(1, limit))
        orders = session.exec(stmt).all()

        result = []
        for o in orders:
            items = []
            for it in (o.items or []):
                prod = it.product
                items.append(
                    {
                        "product_id": it.product_id,
                        "quantity": int(it.quantity),
                        "product_name": getattr(prod, "name", None),
                        "product_price": float(getattr(prod, "price", 0.0))
                        if prod is not None
                        else None,
                    }
                )
            result.append(
                {
                    "order_id": o.order_id,
                    "user_id": o.user_id,
                    "status": o.status,
                    "items": items,
                }
            )
        return result


def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    """Get order by ID.

    Args:
        order_id (int): Order ID to retrieve.

    Returns:
        Optional[Dict[str, Any]]: Order dictionary if found, None otherwise.
    """
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            return None
        items = []
        for it in (order.items or []):
            prod = it.product
            items.append(
                {
                    "product_id": it.product_id,
                    "quantity": int(it.quantity),
                    "product_name": getattr(prod, "name", None),
                    "product_price": float(getattr(prod, "price", 0.0))
                    if prod is not None
                    else None,
                }
            )
        return {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "status": order.status,
            "items": items,
        }


def get_user_orders(user_id: str) -> List[Dict[str, Any]]:
    """Get orders for a specific user.

    Args:
        user_id (int): User ID to filter orders by.

    Returns:
        List[Dict[str, Any]]: List of order dictionaries for the specified user.
    """
    return get_orders(user_id=user_id, limit=100)  # Arbitrary limit for user orders


def get_order_items(limit: int = 25) -> List[Dict[str, Any]]:
    """List order items with optional limit.

    Args:
        limit (int, optional): Maximum number of order items to return. Defaults to 25.

    Returns:
        List[Dict[str, Any]]: List of order item dictionaries.
    """
    with Session(engine) as session:
        stmt = select(OrderItem, Order).join(
            Order, OrderItem.order_id == Order.order_id).limit(max(1, limit))
        results = session.exec(stmt).all()
        return [
            {
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": int(item.quantity),
                "status": order.status,
            }
            for item, order in results
        ]


def get_order_items_by_order_id(order_id: str) -> List[Dict[str, Any]]:
    """Get all order items for a given order ID, including order status from the Order entity.

    Args:
        order_id (str): Order ID to retrieve order items for.

    Returns:
        List[Dict[str, Any]]: List of order item dictionaries for the specified order.
    """
    with Session(engine) as session:
        stmt = select(OrderItem, Order).join(Order, OrderItem.order_id ==
                                             Order.order_id).where(OrderItem.order_id == order_id)
        results = session.exec(stmt).all()
        return [
            {
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": int(item.quantity),
                "status": order.status,
            }
            for item, order in results
        ]


def get_order_items_by_status(status: str) -> List[Dict[str, Any]]:
    """Get order items by status.

    Args:
        status (str): Status to filter order items by.

    Returns:
        List[Dict[str, Any]]: List of order item dictionaries with the specified status.
    """
    with Session(engine) as session:
        stmt = select(OrderItem, Order).join(
            Order, OrderItem.order_id == Order.order_id).where(Order.status == status)
        results = session.exec(stmt).all()
        return [
            {
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": int(item.quantity),
                "status": order.status,
            }
            for item, order in results
        ]


def get_order_items_by_product(product_id: str) -> List[Dict[str, Any]]:
    """Get order items by product ID.

    Args:
        product_id (str): Product ID to filter order items by.

    Returns:
        List[Dict[str, Any]]: List of order item dictionaries for the specified product.
    """
    with Session(engine) as session:
        stmt = select(OrderItem, Order).join(Order, OrderItem.order_id ==
                                             Order.order_id).where(OrderItem.product_id == product_id)
        results = session.exec(stmt).all()
        return [
            {
                "order_id": item.order_id,
                "product_id": item.product_id,
                "quantity": int(item.quantity),
                "status": order.status,
            }
            for item, order in results
        ]
