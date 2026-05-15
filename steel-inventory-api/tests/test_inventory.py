import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_get_all_products():
    """Test getting all products"""
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ==================== Search by Grade Tests ====================
# These tests verify the search-by-grade feature functionality


@pytest.fixture
def setup_test_products():
    """Set up test products with various grades for search testing"""
    # Clear database
    db.products = []
    db._next_id = 1

    # Create test products with different grades
    test_products = [
        {
            "product_code": "STL-A36-001",
            "grade": "A36",
            "shape": "sheet",
            "length_mm": 2400,
            "width_mm": 1200,
            "thickness_mm": 6.0,
            "quantity": 100,
            "location": "Warehouse-A",
        },
        {
            "product_code": "STL-A36-002",
            "grade": "A36",
            "shape": "plate",
            "length_mm": 3000,
            "width_mm": 1500,
            "thickness_mm": 10.0,
            "quantity": 50,
            "location": "Warehouse-B",
        },
        {
            "product_code": "STL-304-001",
            "grade": "304",
            "shape": "coil",
            "length_mm": 5000,
            "thickness_mm": 2.0,
            "quantity": 200,
            "location": "Warehouse-A",
        },
        {
            "product_code": "STL-4140-001",
            "grade": "4140",
            "shape": "bar",
            "length_mm": 6000,
            "thickness_mm": 25.0,
            "quantity": 75,
            "location": "Warehouse-C",
        },
    ]

    for product_data in test_products:
        db.create(product_data)

    yield

    # Cleanup after tests
    db.products = []
    db._next_id = 1


def test_search_by_grade_existing_single_result(setup_test_products):
    """Test searching for a grade that exists with single result"""
    response = client.get("/inventory/?grade=304")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["grade"] == "304"
    assert results[0]["product_code"] == "STL-304-001"


def test_search_by_grade_existing_multiple_results(setup_test_products):
    """Test searching for a grade that exists with multiple results"""
    response = client.get("/inventory/?grade=A36")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 2

    # Verify all results match the search grade
    for product in results:
        assert product["grade"] == "A36"

    # Verify we got the expected products
    product_codes = [p["product_code"] for p in results]
    assert "STL-A36-001" in product_codes
    assert "STL-A36-002" in product_codes


def test_search_by_grade_non_existent(setup_test_products):
    """Test searching for a grade that doesn't exist returns empty list"""
    response = client.get("/inventory/?grade=9999")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 0


def test_search_by_grade_case_insensitive_lowercase(setup_test_products):
    """Test searching for grade is case-insensitive (lowercase input)"""
    response = client.get("/inventory/?grade=a36")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 2

    # Verify all results match A36 regardless of case
    for product in results:
        assert product["grade"].upper() == "A36"


def test_search_by_grade_case_insensitive_mixed_case(setup_test_products):
    """Test searching for grade is case-insensitive (mixed case input)"""
    response = client.get("/inventory/?grade=a36")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2

    # Same test with different case
    response_upper = client.get("/inventory/?grade=A36")
    assert response_upper.status_code == 200
    results_upper = response_upper.json()

    # Both searches should return the same results
    assert len(results) == len(results_upper)
    assert sorted([p["id"] for p in results]) == sorted([p["id"] for p in results_upper])


def test_search_by_grade_empty_database():
    """Test searching when database is empty returns empty list"""
    # Clear database
    db.products = []
    db._next_id = 1

    response = client.get("/inventory/?grade=A36")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 0

    # Cleanup
    db.products = []
    db._next_id = 1


def test_search_by_grade_with_special_characters(setup_test_products):
    """Test searching for grade with numeric characters works correctly"""
    response = client.get("/inventory/?grade=4140")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["grade"] == "4140"
    assert results[0]["product_code"] == "STL-4140-001"


def test_get_all_products_without_grade_filter(setup_test_products):
    """Test that getting all products without grade filter still works"""
    response = client.get("/inventory/")

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 4  # All products should be returned


# TODO: Add more comprehensive tests:
# - test_create_product_success
# - test_create_product_duplicate_code
# - test_update_product_negative_quantity
# - test_delete_product
# - test_weight_calculation_sheet
# - test_weight_calculation_invalid_shape
