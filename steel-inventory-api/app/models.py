from pydantic import BaseModel, Field, PrivateAttr, computed_field
from typing import Optional, Literal
from datetime import datetime
from app.config import DEFAULT_INVENTORY_THRESHOLD
from app.utils.steel_utils import is_low_stock

QualityGrade = Literal["Premium", "Standard", "Economy"]


class SteelProduct(BaseModel):
    """Model for steel product in inventory"""

    id: Optional[int] = None
    product_code: str = Field(..., min_length=3, max_length=20)
    grade: str  # e.g., "A36", "304", "4140"
    shape: Literal["sheet", "coil", "plate", "bar", "tube"]
    length_mm: float = Field(..., gt=0)
    width_mm: Optional[float] = Field(None, gt=0)
    thickness_mm: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    inventory_threshold: Optional[int] = Field(None, ge=0)
    location: str
    quality_grade: QualityGrade = "Standard"
    last_updated: Optional[datetime] = None
    _default_inventory_threshold: int = PrivateAttr(default=DEFAULT_INVENTORY_THRESHOLD)

    def set_default_inventory_threshold(self, threshold: int) -> "SteelProduct":
        self._default_inventory_threshold = threshold
        return self

    @computed_field(return_type=bool)
    @property
    def is_low_stock(self) -> bool:
        return is_low_stock(
            self.quantity,
            self.inventory_threshold,
            self._default_inventory_threshold,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "product_code": "STL-001",
                "grade": "A36",
                "shape": "sheet",
                "length_mm": 2400,
                "width_mm": 1200,
                "thickness_mm": 6.0,
                "quantity": 150,
                "inventory_threshold": 75,
                "location": "Warehouse-A",
                "quality_grade": "Standard",
            }
        }


class SteelProductCreate(BaseModel):
    product_code: str
    grade: str
    shape: Literal["sheet", "coil", "plate", "bar", "tube"]
    length_mm: float
    width_mm: Optional[float] = None
    thickness_mm: float
    quantity: int = Field(..., ge=0)
    inventory_threshold: Optional[int] = Field(None, ge=0)
    location: str
    quality_grade: QualityGrade = "Standard"


class SteelProductUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    quality_grade: Optional[QualityGrade] = None
    inventory_threshold: Optional[int] = Field(None, ge=0)


class InventoryThresholdConfig(BaseModel):
    threshold: int = Field(..., ge=0)


class LowStockResponse(BaseModel):
    threshold: int
    count: int
    products: list[SteelProduct]


# TODO: Add models for batch tracking, quality inspections
