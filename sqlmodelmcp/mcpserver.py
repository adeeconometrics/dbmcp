# mcpserver.py
from typing import List, Optional, Dict, Any
import argparse

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from sqlmodel import Session, select

from db import engine
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem


# -----------------------
# Business-logic (impls)
# -----------------------

def list_users_impl(limit: int = 25) -> List[Dict[str, Any]]:
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
                "user_id": u.user_id,
                "name": u.name,
                "email": u.email,
                "order_ids": [o.order_id for o in (u.orders or [])],
            }
            for u in users
        ]


def list_products_impl(limit: int = 50) -> List[Dict[str, Any]]:
    """List products with optional limit.

    Args:
        limit (int, optional): Maximum number of products to return. Defaults to 50.

    Returns:
        List[Dict[str, Any]]: List of product dictionaries.
    """
    with Session(engine) as session:
        stmt = select(Product).limit(max(1, limit))
        prods = session.exec(stmt).all()
        return [
            {
                "product_id": p.product_id,
                "name": p.name,
                "price": float(p.price),
                "stock_quantity": int(p.stock_quantity),
            }
            for p in prods
        ]


def search_products_impl(q: str, limit: int = 25) -> List[Dict[str, Any]]:
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
                "product_id": p.product_id,
                "name": p.name,
                "price": float(p.price),
                "stock_quantity": int(p.stock_quantity),
            }
            for p in prods
        ]


def list_orders_impl(
    limit: int = 25, user_id: Optional[int] = None
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


def get_order_impl(order_id: int) -> Optional[Dict[str, Any]]:
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


# -----------------------
# Unified FastAPI + MCP
# -----------------------

app = FastAPI()


# @mcp.tool()
# def list_users(limit: int = 25) -> List[Dict[str, Any]]:
#     return list_users_impl(limit)


# @mcp.tool()
# def list_products(limit: int = 50) -> List[Dict[str, Any]]:
#     return list_products_impl(limit)


# @mcp.tool()
# def search_products(q: str, limit: int = 25) -> List[Dict[str, Any]]:
#     return search_products_impl(q, limit)


# @mcp.tool()
# def list_orders(
#     limit: int = 25, user_id: Optional[int] = None
# ) -> List[Dict[str, Any]]:
#     return list_orders_impl(limit=limit, user_id=user_id)


# @mcp.tool()
# def get_order(order_id: int) -> Optional[Dict[str, Any]]:
#     return get_order_impl(order_id)


# -----------------------
# HTTP routes (optional)
# -----------------------

@app.get("/list_users")
def http_list_users(limit: int = 25):
    """Api endpoint to list users with optional limit. Defaults to 25."""
    return list_users_impl(limit)


@app.get("/list_products")
def http_list_products(limit: int = 50):
    """Api endpoint to list products with optional limit. Defaults to 50."""
    return list_products_impl(limit)


@app.get("/search_products")
def http_search_products(q: str, limit: int = 25):
    """Api endpoint to search products with optional limit. Defaults to 25."""
    return search_products_impl(q, limit)


@app.get("/list_orders")
def http_list_orders(limit: int = 25, user_id: Optional[int] = None):
    """Api endpoint to list orders with optional limit and user filter."""
    return list_orders_impl(limit=limit, user_id=user_id)


@app.get("/orders/{order_id}")
def http_get_order(order_id: int):
    """Api endpoint to get order by ID."""
    order = get_order_impl(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


mcp = FastApiMCP(app, "dbtools")
mcp.mount()

# -----------------------
# CLI entrypoint
# -----------------------


def main():
    """Run the MCP+FastAPI server."""
    parser = argparse.ArgumentParser(description="Run MCP+FastAPI server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
