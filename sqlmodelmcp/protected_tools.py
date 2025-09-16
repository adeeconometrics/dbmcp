from typing import Any, Dict, List, Optional, Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from auth import get_current_user
from auth_middleware import require_authentication
from db import engine
from models import User, Product, Order, Category, OrderItem, User as UserModel


# Protected user operations (require authentication)
def get_authenticated_user_orders(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> List[Dict[str, Any]]:
    """Get orders for the authenticated user only."""
    with Session(engine) as session:
        stmt = select(Order).where(Order.user_id ==
                                   current_user.user_id).limit(100)
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
                    "order_date": o.order_date,
                    "items": items,
                }
            )
        return result


def get_authenticated_user_profile(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> Dict[str, Any]:
    """Get the authenticated user's profile information."""
    return {
        "user_id": current_user.user_id,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "address_id": current_user.address_id,
        "payment_info": current_user.payment_info
    }


def verify_user_access_to_order(
    order_id: str,
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> Optional[Dict[str, Any]]:
    """Get order by ID, but only if it belongs to the authenticated user."""
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            return None

        # Check if the order belongs to the authenticated user
        if order.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this order"
            )

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
            "order_date": order.order_date,
            "items": items,
        }


# Admin-level functions (these would require admin authentication in a real system)
def get_all_users_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25
) -> List[Dict[str, Any]]:
    """List all users (admin function - in real app, check for admin role)."""
    # In a real application, you would check if current_user has admin privileges
    with Session(engine) as session:
        stmt = select(User).limit(max(1, limit))
        users = session.exec(stmt).all()
        return [
            {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "user_id": user.user_id,
                "created_at": user.created_at,
            }
            for user in users
        ]


def get_all_orders_admin(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    limit: int = 25,
    user_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List all orders (admin function - in real app, check for admin role)."""
    # In a real application, you would check if current_user has admin privileges
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
                    "order_date": o.order_date,
                    "items": items,
                }
            )
        return result


# Public functions (no authentication required)
def get_public_products(limit: int = 50) -> List[Dict[str, Any]]:
    """List products publicly available."""
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


def search_public_products(q: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Search for products by name (public)."""
    with Session(engine) as session:
        stmt = select(Product, Category).join(
            Category, Product.category_id == Category.category_id
        ).where(Product.name.ilike(f"%{q}%")).limit(max(1, limit))
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
