from typing import Optional
import argparse

from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from tools import (
    list_users_impl,
    list_products_impl,
    search_products_impl,
    list_orders_impl,
    get_order_impl,
)

app = FastAPI()


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
