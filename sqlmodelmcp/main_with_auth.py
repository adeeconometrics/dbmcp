from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List, Dict, Any, Optional

# Import authentication modules
from auth_routes import router as auth_router
from auth import get_current_user
from models import User as UserModel

# Import protected and public tools
from protected_tools import (
    get_authenticated_user_orders,
    get_authenticated_user_profile,
    verify_user_access_to_order,
    get_all_users_admin,
    get_all_orders_admin,
    get_public_products,
    search_public_products
)

# Import original tools for backward compatibility (these should be protected in production)
from tools import (
    get_products,
    get_products_by_name,
    get_orders,
    get_order_by_id,
    get_users,
    get_user_by_id
)

app = FastAPI(
    title="MCP Database API with Authentication",
    description="A FastAPI application with JWT authentication and database operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Public endpoints (no authentication required)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "MCP Database API with Authentication",
        "version": "1.0.0",
        "docs": "/docs",
        "auth_endpoints": {
            "register": "/auth/register",
            "login": "/auth/token",
            "profile": "/auth/me"
        }
    }


@app.get("/public/products", response_model=List[Dict[str, Any]])
async def list_public_products(limit: int = 50):
    """List products publicly (no authentication required)."""
    return get_public_products(limit=limit)


@app.get("/public/products/search", response_model=List[Dict[str, Any]])
async def search_products_public(q: str, limit: int = 25):
    """Search products publicly (no authentication required)."""
    return search_public_products(q=q, limit=limit)

# Protected user endpoints (require authentication)


@app.get("/user/orders", response_model=List[Dict[str, Any]])
async def get_my_orders(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Get orders for the authenticated user."""
    return get_authenticated_user_orders(current_user)


@app.get("/user/profile", response_model=Dict[str, Any])
async def get_my_profile(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Get profile for the authenticated user."""
    return get_authenticated_user_profile(current_user)


@app.get("/user/orders/{order_id}", response_model=Dict[str, Any])
async def get_my_order(
    order_id: str,
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Get a specific order for the authenticated user."""
    order = verify_user_access_to_order(order_id, current_user)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

# Admin endpoints (require authentication - in production, add role-based access)


@app.get("/admin/users", response_model=List[Dict[str, Any]])
async def list_all_users(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25
):
    """List all users (admin endpoint)."""
    return get_all_users_admin(current_user, limit=limit)


@app.get("/admin/orders", response_model=List[Dict[str, Any]])
async def list_all_orders(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25,
    user_id: Optional[str] = None
):
    """List all orders (admin endpoint)."""
    return get_all_orders_admin(current_user, limit=limit, user_id=user_id)

# Legacy endpoints (backward compatibility - consider protecting these in production)


@app.get("/legacy/products", response_model=List[Dict[str, Any]])
async def legacy_get_products(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 50
):
    """Legacy product listing (requires authentication)."""
    return get_products(limit=limit)


@app.get("/legacy/products/search", response_model=List[Dict[str, Any]])
async def legacy_search_products(
    q: str,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25
):
    """Legacy product search (requires authentication)."""
    return get_products_by_name(q=q, limit=limit)


@app.get("/legacy/orders", response_model=List[Dict[str, Any]])
async def legacy_get_orders(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25,
    user_id: Optional[str] = None
):
    """Legacy order listing (requires authentication)."""
    return get_orders(limit=limit, user_id=user_id)


@app.get("/legacy/orders/{order_id}", response_model=Optional[Dict[str, Any]])
async def legacy_get_order(
    order_id: str,
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Legacy order retrieval (requires authentication)."""
    return get_order_by_id(order_id)


@app.get("/legacy/users", response_model=List[Dict[str, Any]])
async def legacy_get_users(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25
):
    """Legacy user listing (requires authentication)."""
    return get_users(limit=limit)


@app.get("/legacy/users/{user_id}", response_model=Optional[Dict[str, Any]])
async def legacy_get_user(
    user_id: str,
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Legacy user retrieval (requires authentication)."""
    return get_user_by_id(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
