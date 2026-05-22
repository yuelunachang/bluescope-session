from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import LowStockResponse, SteelProduct, SteelProductCreate, SteelProductUpdate
from app.database import db
from app.utils.steel_utils import is_low_stock

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.get("/", response_model=List[SteelProduct])
async def get_all_products():
    """Get all products in inventory"""
    return db.get_all()


@router.get("/low-stock", response_model=LowStockResponse)
async def get_low_stock_products():
    """Get all products below their effective inventory threshold"""
    products = [
        product
        for product in db.get_all()
        if is_low_stock(
            product.quantity,
            product.inventory_threshold,
            db.global_inventory_threshold,
        )
    ]
    return {
        "threshold": db.global_inventory_threshold,
        "count": len(products),
        "products": products,
    }

@router.get("/{product_id}", response_model=SteelProduct)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    product = db.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product

@router.post("/", response_model=SteelProduct, status_code=status.HTTP_201_CREATED)
async def create_product(product: SteelProductCreate):
    """Create a new product in inventory"""
    # TODO: Add validation using steel_utils
    product_dict = product.model_dump()
    return db.create(product_dict)

@router.patch("/{product_id}", response_model=SteelProduct)
async def update_product(product_id: int, update: SteelProductUpdate):
    """Update product quantity or location"""
    # BUG: No validation for negative quantities
    update_data = update.model_dump(exclude_unset=True)
    product = db.update(product_id, update_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    """Delete a product from inventory"""
    if not db.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

# TODO: Add endpoints for:
# - Search/filter by grade, location, shape
# - Bulk operations
