# BlueScope Steel Inventory Management API

A FastAPI-based inventory management system for steel products with a modern web interface.

## Setup

```powershell
python -m venv venv
. .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m uvicorn app.main:app --reload
```

## Access the Application

- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

## Features (Partial Implementation)

- ✅ Modern web interface with real-time inventory display
- ✅ Dashboard with statistics
- ✅ Product filtering and search
- ✅ Low-inventory monitoring with dashboard count, product badges, and low-stock filtering
- [ ] CRUD operations for steel inventory (basic implementation)
- [ ] Weight and dimension calculations
- [x] Inventory level alerts
- [ ] Grade specifications
- [ ] Batch tracking

## Low-Inventory Monitoring

Products now expose an `is_low_stock` flag from the API. A product is low stock when its `quantity` is below its effective threshold:

- product-specific `inventory_threshold`, when present
- otherwise the global default inventory threshold

The frontend uses that backend flag to:

- show a `⚠ Low Stock` badge on product cards
- power the **⚠ Low Stock Only** filter button
- populate the **⚠ Low Stock Items** dashboard widget

### Inventory Threshold Configuration

The current global threshold can be read and updated at runtime without redeploying:

```http
GET /config/inventory-threshold
PUT /config/inventory-threshold
PUT /api/config/inventory-threshold
```

Example request:

```json
{
  "threshold": 100
}
```

### Low-Stock Inventory Endpoint

Use the dedicated low-stock endpoint to retrieve only products that are below their effective threshold:

```http
GET /inventory/low-stock
```

Example response:

```json
{
  "threshold": 50,
  "count": 1,
  "products": [
    {
      "id": 7,
      "product_code": "STL-007",
      "quantity": 45,
      "inventory_threshold": null,
      "is_low_stock": true
    }
  ]
}
```

## Sample Data

The application comes pre-loaded with 10 steel products across different:
- **Shapes:** Sheet, Coil, Plate, Bar, Tube
- **Grades:** A36, 304, 316, 4140
- **Locations:** Warehouse-A, Warehouse-B, Warehouse-C
