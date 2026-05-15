---
name: cost-estimation
description: "Calculate material costs, shipping expenses, and total project estimates for steel products. Use when: estimating project costs; calculating material spend; computing shipping expenses; comparing pricing scenarios; generating cost breakdowns for steel orders."
author: bluescope
version: 1.0.0
agentSkillsVersion: 0.1.0
argument-hint: "Provide product details (grade, dimensions, quantity), unit price, and shipping parameters"
---

# Cost Estimation Skill

Calculates material costs, shipping expenses, and total project estimates for steel products across different pricing scenarios.

## When to Use

- Estimating total cost for a steel order
- Comparing pricing across different suppliers or scenarios
- Generating cost breakdowns for quotes or budgets
- Calculating shipping expenses based on weight and distance

## Formulas

### Material Cost
```
Material Cost = Unit Weight (kg) × Quantity × Steel Price ($/kg)
```

### Shipping Cost
```
Shipping Cost = Total Weight (kg) × Shipping Rate ($/kg/100km) × Distance (km) / 100
Total Weight  = Unit Weight (kg) × Quantity
```

### Total Project Cost
```
Total Cost = Material Cost + Shipping Cost
Cost per Unit = Total Cost / Quantity
```

## Procedure

1. **Gather inputs** — collect the following from the user:
   - Product grade and dimensions (length × width × thickness in mm)
   - Quantity (number of units)
   - Unit weight (kg) — calculate if not provided: `Volume (m³) × Density (kg/m³)`
     - Steel density: ~7850 kg/m³
     - Volume (m³) = (L × W × T) / 1,000,000,000  *(dimensions in mm)*
   - Steel price per kg ($/kg)
   - Shipping distance (km)
   - Shipping rate ($/kg/100km)

2. **Calculate material cost**
   - `material_cost = unit_weight × quantity × steel_price`

3. **Calculate shipping cost**
   - `total_weight = unit_weight × quantity`
   - `shipping_cost = total_weight × shipping_rate × distance / 100`

4. **Calculate total cost**
   - `total_cost = material_cost + shipping_cost`
   - `cost_per_unit = total_cost / quantity`

5. **Present results** in a clear breakdown showing each component and the totals.

## Pricing Scenarios

Apply the following multipliers when the user specifies a scenario:

| Scenario      | Material Multiplier | Shipping Multiplier | Notes                          |
|---------------|--------------------|--------------------|-------------------------------|
| Standard      | 1.00               | 1.00               | Default market rate            |
| Premium Rush  | 1.15               | 1.30               | Priority processing + express  |
| Bulk Discount | 0.92               | 0.95               | Orders > 100 units             |
| Export        | 1.05               | 1.20               | Additional compliance costs    |

## Usage Examples

### Example 1 — Basic Estimate

**Input:**
- Product: A36 plate, 3000 × 1500 × 10 mm
- Quantity: 50 units
- Unit weight: 353.25 kg
- Steel price: $0.85/kg
- Shipping: 500 km at $0.12/kg/100 km

**Calculation:**
```
Material Cost = 353.25 × 50 × 0.85        = $15,013.13
Total Weight  = 353.25 × 50               = 17,662.5 kg
Shipping Cost = 17,662.5 × 0.12 × 500/100 = $10,597.50
Total Cost    = $15,013.13 + $10,597.50   = $25,610.63
Cost per Unit = $25,610.63 / 50           = $512.21
```

### Example 2 — Bulk Discount Scenario

Same order as above with Bulk Discount (>100 units, but applied here as demonstration):
```
Material Cost = $15,013.13 × 0.92 = $13,812.08
Shipping Cost = $10,597.50 × 0.95 = $10,067.63
Total Cost    = $23,879.71
Cost per Unit = $477.59
Savings       = $1,731.92 vs Standard
```

### Example 3 — Unit Weight Calculation from Dimensions

When unit weight is not provided, calculate it first:
```
Dimensions: 3000 × 1500 × 10 mm
Volume = (3000 × 1500 × 10) / 1,000,000,000 = 0.045 m³
Weight = 0.045 × 7850 = 353.25 kg
```

## Output Format

Present results in the following structure:

```
## Cost Estimate — [Product Description]

### Inputs
| Parameter       | Value          |
|-----------------|----------------|
| Product         | ...            |
| Quantity        | ... units      |
| Unit Weight     | ... kg         |
| Total Weight    | ... kg         |
| Steel Price     | $... /kg       |
| Shipping Rate   | $... /kg/100km |
| Distance        | ... km         |
| Scenario        | Standard       |

### Cost Breakdown
| Component       | Amount         |
|-----------------|----------------|
| Material Cost   | $...           |
| Shipping Cost   | $...           |
| **Total Cost**  | **$...**       |
| Cost per Unit   | $...           |
```
