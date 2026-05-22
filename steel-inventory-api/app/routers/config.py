from fastapi import APIRouter

from app.database import db
from app.models import InventoryThresholdConfig

router = APIRouter(
    prefix="/config",
    tags=["config"]
)

api_router = APIRouter(
    prefix="/api/config",
    tags=["config"]
)


@router.get("/inventory-threshold", response_model=InventoryThresholdConfig)
@api_router.get("/inventory-threshold", response_model=InventoryThresholdConfig)
async def get_inventory_threshold():
    return {"threshold": db.global_inventory_threshold}


@router.put("/inventory-threshold", response_model=InventoryThresholdConfig)
@api_router.put("/inventory-threshold", response_model=InventoryThresholdConfig)
async def update_inventory_threshold(config: InventoryThresholdConfig):
    db.set_global_inventory_threshold(config.threshold)
    return {"threshold": db.global_inventory_threshold}
