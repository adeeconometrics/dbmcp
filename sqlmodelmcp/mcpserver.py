from typing import Optional
import argparse

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from tools import (
    get_users,
    get_user_by_id,
    get_products,
    get_products_by_name,
    get_orders,
    get_order_by_id,
    get_user_orders,
    get_order_items,
    get_order_items_by_order_id,
    get_order_items_by_product,
    get_order_items_by_status,
)

app = FastAPI()


@app.get("/users")
def http_get_users(limit: int = 25):
    """Api endpoint to list users with optional limit. Defaults to 25."""
    return get_users(limit)


@app.get("/users/{user_id}")
def http_get_user_by_id(user_id: str):
    """Api endpoint to get user by ID."""
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/products")
def http_get_products(limit: int = 50):
    """Api endpoint to list products with optional limit. Defaults to 50."""
    return get_products(limit)


@app.get("/search_products/{item}")
def http_search_products(item: str, limit: int = 25):
    """Api endpoint to search products with optional limit. Defaults to 25."""
    return get_products_by_name(item, limit)


@app.get("/orders")
def http_get_orders(limit: int = 25, user_id: Optional[int] = None):
    """Api endpoint to get orders with optional limit and user filter."""
    return get_orders(limit=limit, user_id=user_id)


@app.get("/orders/{order_id}")
def http_get_order_by_id(order_id: str):
    """Api endpoint to get order by ID."""
    order = get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/users/{user_id}/orders")
def http_get_user_orders(user_id: str):
    """Api endpoint to get orders for a specific user."""
    return get_user_orders(user_id=user_id)


@app.get("/order_items")
def http_get_order_items(limit: int = 25):
    """Api endpoint to list order items with optional limit. Defaults to 25."""
    return get_order_items(limit)


@app.get("/order_items/{item_id}")
def http_get_order_items_by_order_id(item_id: str):
    """Api endpoint to get order items by ID."""
    items = get_order_items_by_order_id(item_id)
    if not items:
        raise HTTPException(status_code=404, detail="Order item not found")
    return items


@app.get("/order_items/product/{product_id}")
def http_get_order_items_by_product(product_id: str):
    """Api endpoint to get order items by product ID."""
    items = get_order_items_by_product(product_id)
    if not items:
        raise HTTPException(
            status_code=404, detail="Order items for product not found")
    return items


@app.get("/order_items/status/{status}")
def http_get_order_items_by_status(status: str):
    """Api endpoint to get order items by status."""
    items = get_order_items_by_status(status)
    if not items:
        raise HTTPException(
            status_code=404, detail="Order items with status not found")
    return items


mcp = FastApiMCP(app, "dbtools")
mcp.mount()


def main():
    """Run the MCP via FastAPI server."""
    parser = argparse.ArgumentParser(description="Run MCP via FastAPI server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
