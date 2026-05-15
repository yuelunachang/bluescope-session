"""Utility functions for steel product calculations.

Shapes and their dimension conventions:
  sheet / plate : length × width × thickness  (all rectangular)
  coil          : length × width × thickness  (strip unrolled; same formula as sheet)
  bar           : length, thickness = diameter (solid circular cross-section)
  tube          : length, width_mm = outer diameter, thickness_mm = wall thickness
                  (hollow circular cross-section)
"""

import math
from typing import Optional

# Steel density in kg/mm³ (approximate for carbon steel)
STEEL_DENSITY_KG_MM3: float = 7.85e-6

VALID_GRADES: tuple[str, ...] = ("A36", "A572", "A992", "304", "316", "316L", "4140", "4340", "1018", "1045")

VALID_SHAPES: tuple[str, ...] = ("sheet", "plate", "coil", "bar", "tube")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_positive(value: float, name: str) -> None:
    """Raise ValueError if *value* is not strictly positive.

    Args:
        value: The numeric value to check.
        name:  Human-readable field name used in the error message.

    Raises:
        ValueError: If *value* is zero or negative.
    """
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero, got {value}")


def _validate_required(value: Optional[float], name: str) -> float:
    """Raise ValueError if *value* is None, otherwise return it.

    Args:
        value: The value to check.
        name:  Human-readable field name used in the error message.

    Returns:
        The non-None value.

    Raises:
        ValueError: If *value* is None.
    """
    if value is None:
        raise ValueError(f"{name} is required for this shape")
    return value


# ---------------------------------------------------------------------------
# Private shape-specific weight calculators
# ---------------------------------------------------------------------------

def _weight_sheet_plate(length_mm: float, width_mm: float, thickness_mm: float) -> float:
    """Calculate weight of a rectangular flat product (sheet or plate).

    Formula: volume = length × width × thickness

    Args:
        length_mm:    Length in millimetres.
        width_mm:     Width in millimetres.
        thickness_mm: Thickness in millimetres.

    Returns:
        Weight in kilograms, rounded to 2 decimal places.
    """
    volume_mm3 = length_mm * width_mm * thickness_mm
    return round(volume_mm3 * STEEL_DENSITY_KG_MM3, 2)


def _weight_coil(length_mm: float, width_mm: float, thickness_mm: float) -> float:
    """Calculate weight of a steel coil (strip unrolled to flat dimensions).

    The coil is treated as an unrolled strip; its weight is identical to a
    sheet of the same length, width, and thickness.

    Formula: volume = length × width × thickness

    Args:
        length_mm:    Total unrolled strip length in millimetres.
        width_mm:     Strip width in millimetres.
        thickness_mm: Strip thickness (gauge) in millimetres.

    Returns:
        Weight in kilograms, rounded to 2 decimal places.
    """
    volume_mm3 = length_mm * width_mm * thickness_mm
    return round(volume_mm3 * STEEL_DENSITY_KG_MM3, 2)


def _weight_bar(length_mm: float, thickness_mm: float) -> float:
    """Calculate weight of a solid circular bar.

    Formula: volume = π × (diameter / 2)² × length

    Args:
        length_mm:    Length of the bar in millimetres.
        thickness_mm: Diameter of the bar in millimetres.

    Returns:
        Weight in kilograms, rounded to 2 decimal places.
    """
    radius_mm = thickness_mm / 2
    volume_mm3 = math.pi * radius_mm ** 2 * length_mm
    return round(volume_mm3 * STEEL_DENSITY_KG_MM3, 2)


def _weight_tube(length_mm: float, outer_diameter_mm: float, wall_thickness_mm: float) -> float:
    """Calculate weight of a hollow circular tube.

    Convention (Option A): width_mm = outer diameter, thickness_mm = wall thickness.

    Formula: volume = π × ((OD/2)² − (ID/2)²) × length
             where ID = OD − 2 × wall_thickness

    Args:
        length_mm:         Length of the tube in millimetres.
        outer_diameter_mm: Outer diameter in millimetres (mapped from width_mm).
        wall_thickness_mm: Wall thickness in millimetres (mapped from thickness_mm).

    Returns:
        Weight in kilograms, rounded to 2 decimal places.

    Raises:
        ValueError: If wall thickness is >= half the outer diameter (no material).
    """
    inner_diameter_mm = outer_diameter_mm - 2 * wall_thickness_mm
    if inner_diameter_mm <= 0:
        raise ValueError(
            f"Wall thickness ({wall_thickness_mm} mm) must be less than "
            f"half the outer diameter ({outer_diameter_mm / 2} mm)"
        )
    outer_radius = outer_diameter_mm / 2
    inner_radius = inner_diameter_mm / 2
    volume_mm3 = math.pi * (outer_radius ** 2 - inner_radius ** 2) * length_mm
    return round(volume_mm3 * STEEL_DENSITY_KG_MM3, 2)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate_weight_kg(
    length_mm: float,
    width_mm: Optional[float],
    thickness_mm: float,
    shape: str,
) -> float:
    """Calculate the weight of a steel product in kilograms.

    Dispatches to a shape-specific calculator after validating inputs.

    Dimension conventions by shape:
      - sheet / plate : width_mm required; thickness_mm = sheet thickness
      - coil          : width_mm required; thickness_mm = strip gauge
      - bar           : width_mm not used; thickness_mm = bar diameter
      - tube          : width_mm = outer diameter; thickness_mm = wall thickness

    Args:
        length_mm:    Length of the product in millimetres. Must be > 0.
        width_mm:     Width in millimetres (shape-dependent, see above).
        thickness_mm: Thickness / diameter / wall thickness in millimetres. Must be > 0.
        shape:        Product shape. Must be one of: sheet, plate, coil, bar, tube.

    Returns:
        Weight in kilograms, rounded to 2 decimal places.

    Raises:
        ValueError:  If any required dimension is missing or non-positive, or if
                     the shape string is not recognised.
    """
    if shape not in VALID_SHAPES:
        raise ValueError(f"Unknown shape '{shape}'. Must be one of: {', '.join(VALID_SHAPES)}")

    _validate_positive(length_mm, "length_mm")
    _validate_positive(thickness_mm, "thickness_mm")

    if shape in ("sheet", "plate"):
        w = _validate_required(width_mm, "width_mm")
        _validate_positive(w, "width_mm")
        return _weight_sheet_plate(length_mm, w, thickness_mm)

    if shape == "coil":
        w = _validate_required(width_mm, "width_mm")
        _validate_positive(w, "width_mm")
        return _weight_coil(length_mm, w, thickness_mm)

    if shape == "bar":
        return _weight_bar(length_mm, thickness_mm)

    # shape == "tube"
    w = _validate_required(width_mm, "width_mm")
    _validate_positive(w, "width_mm")
    return _weight_tube(length_mm, w, thickness_mm)


def validate_grade(grade: str) -> bool:
    """Check whether a steel grade string is recognised.

    Comparison is case-sensitive to match standard grade designations
    (e.g. "A36" is valid, "a36" is not).

    Args:
        grade: Steel grade identifier (e.g. "A36", "304", "4140").

    Returns:
        True if the grade is in the recognised list, False otherwise.
    """
    return grade in VALID_GRADES


def calculate_area_m2(length_mm: float, width_mm: Optional[float]) -> float:
    """Calculate the surface area of a flat product in square metres.

    Args:
        length_mm: Length in millimetres. Must be > 0.
        width_mm:  Width in millimetres. Must be provided and > 0.

    Returns:
        Surface area in square metres, rounded to 2 decimal places.

    Raises:
        ValueError: If width_mm is None or either dimension is non-positive.
    """
    _validate_positive(length_mm, "length_mm")
    w = _validate_required(width_mm, "width_mm")
    _validate_positive(w, "width_mm")
    area_m2 = (length_mm * w) / 1_000_000
    return round(area_m2, 2)
