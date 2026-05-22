import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    db.reset()
    yield
    db.reset()


def replace_inventory(products):
    db.products = []
    db._next_id = 1
    for product in products:
        db.create(product)

def test_root_endpoint():
    """Test the root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_all_products():
    """Test getting all products"""
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_low_stock_endpoint_returns_below_threshold():
    replace_inventory([
        {
            "product_code": "LOW-001",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 49,
            "location": "Warehouse-A",
        },
        {
            "product_code": "LOW-002",
            "grade": "304",
            "shape": "coil",
            "length_mm": 5000,
            "width_mm": 1500,
            "thickness_mm": 3.0,
            "quantity": 50,
            "location": "Warehouse-B",
        },
        {
            "product_code": "LOW-003",
            "grade": "316",
            "shape": "plate",
            "length_mm": 3000,
            "width_mm": 1500,
            "thickness_mm": 10.0,
            "quantity": 10,
            "location": "Warehouse-C",
        },
    ])

    response = client.get("/inventory/low-stock")

    assert response.status_code == 200
    payload = response.json()
    assert payload["threshold"] == 50
    assert payload["count"] == 2
    assert [product["product_code"] for product in payload["products"]] == ["LOW-001", "LOW-003"]


def test_low_stock_endpoint_with_per_product_threshold():
    replace_inventory([
        {
            "product_code": "OVERRIDE-001",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 150,
            "inventory_threshold": 200,
            "location": "Warehouse-A",
        },
        {
            "product_code": "OVERRIDE-002",
            "grade": "304",
            "shape": "coil",
            "length_mm": 5000,
            "width_mm": 1500,
            "thickness_mm": 3.0,
            "quantity": 150,
            "location": "Warehouse-B",
        },
    ])

    response = client.get("/inventory/low-stock")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["products"][0]["product_code"] == "OVERRIDE-001"
    assert payload["products"][0]["is_low_stock"] is True


def test_low_stock_endpoint_empty_when_all_sufficient():
    replace_inventory([
        {
            "product_code": "SAFE-001",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 50,
            "location": "Warehouse-A",
        },
        {
            "product_code": "SAFE-002",
            "grade": "304",
            "shape": "coil",
            "length_mm": 5000,
            "width_mm": 1500,
            "thickness_mm": 3.0,
            "quantity": 120,
            "location": "Warehouse-B",
        },
    ])

    response = client.get("/inventory/low-stock")

    assert response.status_code == 200
    assert response.json() == {"threshold": 50, "count": 0, "products": []}


def test_get_global_threshold_default():
    response = client.get("/config/inventory-threshold")

    assert response.status_code == 200
    assert response.json() == {"threshold": 50}


def test_update_global_threshold():
    replace_inventory([
        {
            "product_code": "THRESH-001",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 75,
            "location": "Warehouse-A",
        },
    ])

    update_response = client.put("/config/inventory-threshold", json={"threshold": 100})
    low_stock_response = client.get("/inventory/low-stock")

    assert update_response.status_code == 200
    assert update_response.json() == {"threshold": 100}
    assert low_stock_response.status_code == 200
    assert low_stock_response.json()["threshold"] == 100
    assert low_stock_response.json()["count"] == 1
    assert low_stock_response.json()["products"][0]["product_code"] == "THRESH-001"


def test_update_global_threshold_invalid():
    response = client.put("/config/inventory-threshold", json={"threshold": -1})

    assert response.status_code == 422


def test_is_low_stock_field_on_product_response():
    low_stock_created = client.post(
        "/inventory/",
        json={
            "product_code": "FIELD-LOW",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 25,
            "inventory_threshold": 30,
            "location": "Warehouse-A",
        },
    )
    sufficient_created = client.post(
        "/inventory/",
        json={
            "product_code": "FIELD-OK",
            "grade": "304",
            "shape": "coil",
            "length_mm": 5000,
            "width_mm": 1500,
            "thickness_mm": 3.0,
            "quantity": 75,
            "location": "Warehouse-B",
        },
    )

    assert low_stock_created.status_code == 201
    assert sufficient_created.status_code == 201

    low_stock_response = client.get(f"/inventory/{low_stock_created.json()['id']}")
    sufficient_response = client.get(f"/inventory/{sufficient_created.json()['id']}")

    assert low_stock_response.status_code == 200
    assert low_stock_response.json()["is_low_stock"] is True
    assert sufficient_response.status_code == 200
    assert sufficient_response.json()["is_low_stock"] is False

# TODO: Add more comprehensive tests:
# - test_create_product_success
# - test_create_product_duplicate_code
# - test_update_product_negative_quantity
# - test_delete_product
# - test_weight_calculation_sheet
# - test_weight_calculation_invalid_shape
