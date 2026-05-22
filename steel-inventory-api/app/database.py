from typing import List, Optional
from app.models import SteelProduct
from datetime import datetime
from app.config import DEFAULT_INVENTORY_THRESHOLD

# Simple in-memory database for the lab
# In production, this would use SQLAlchemy with a real database
class InMemoryDB:
    def __init__(self):
        self.reset()

    def reset(self):
        self.products = []
        self._next_id = 1
        self.global_inventory_threshold = DEFAULT_INVENTORY_THRESHOLD
        self._seed_data()

    def _apply_threshold(self, product: Optional[SteelProduct]) -> None:
        if product:
            product.set_global_inventory_threshold(self.global_inventory_threshold)
    
    def _seed_data(self):
        """Add some initial data"""
        sample_products = [
            SteelProduct(
                id=1,
                product_code="STL-001",
                grade="A36",
                shape="sheet",
                length_mm=2400,
                width_mm=1200,
                thickness_mm=6.0,
                quantity=150,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=2,
                product_code="STL-002",
                grade="304",
                shape="coil",
                length_mm=5000,
                width_mm=1500,
                thickness_mm=3.0,
                quantity=75,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=3,
                product_code="STL-003",
                grade="316",
                shape="plate",
                length_mm=3000,
                width_mm=1500,
                thickness_mm=10.0,
                quantity=50,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=4,
                product_code="STL-004",
                grade="4140",
                shape="bar",
                length_mm=6000,
                width_mm=None,
                thickness_mm=50.0,
                quantity=200,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=5,
                product_code="STL-005",
                grade="A36",
                shape="tube",
                length_mm=4000,
                width_mm=None,
                thickness_mm=5.0,
                quantity=120,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=6,
                product_code="STL-006",
                grade="304",
                shape="sheet",
                length_mm=2400,
                width_mm=1200,
                thickness_mm=4.0,
                quantity=180,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=7,
                product_code="STL-007",
                grade="A36",
                shape="plate",
                length_mm=2500,
                width_mm=1250,
                thickness_mm=12.0,
                quantity=45,
                location="Warehouse-A",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=8,
                product_code="STL-008",
                grade="316",
                shape="coil",
                length_mm=6000,
                width_mm=1800,
                thickness_mm=2.5,
                quantity=60,
                location="Warehouse-B",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=9,
                product_code="STL-009",
                grade="4140",
                shape="bar",
                length_mm=5000,
                width_mm=None,
                thickness_mm=40.0,
                quantity=150,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
            SteelProduct(
                id=10,
                product_code="STL-010",
                grade="304",
                shape="tube",
                length_mm=3500,
                width_mm=None,
                thickness_mm=6.0,
                quantity=90,
                location="Warehouse-C",
                last_updated=datetime.now()
            ),
        ]
        self.products = sample_products
        self._next_id = 11
    
    def get_all(self) -> List[SteelProduct]:
        for product in self.products:
            self._apply_threshold(product)
        return self.products
    
    def get_by_id(self, product_id: int) -> Optional[SteelProduct]:
        for product in self.products:
            if product.id == product_id:
                self._apply_threshold(product)
                return product
        return None
    
    def create(self, product_data: dict) -> SteelProduct:
        # BUG: Missing validation for duplicate product codes
        product = SteelProduct(
            id=self._next_id,
            **product_data,
            last_updated=datetime.now()
        )
        self._apply_threshold(product)
        self.products.append(product)
        self._next_id += 1
        return product
    
    def update(self, product_id: int, update_data: dict) -> Optional[SteelProduct]:
        product = self.get_by_id(product_id)
        if product:
            changed = False
            for key, value in update_data.items():
                if value is not None and getattr(product, key) != value:
                    setattr(product, key, value)
                    changed = True
            if changed:
                product.last_updated = datetime.now()
            self._apply_threshold(product)
            return product
        return None
    
    def delete(self, product_id: int) -> bool:
        # BUG: Missing proper deletion logic
        product = self.get_by_id(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def set_global_inventory_threshold(self, threshold: int) -> int:
        self.global_inventory_threshold = threshold
        return self.global_inventory_threshold

# Global database instance
db = InMemoryDB()
