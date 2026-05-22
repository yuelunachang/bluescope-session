import os


def _load_default_inventory_threshold() -> int:
    value = os.getenv("DEFAULT_INVENTORY_THRESHOLD", "50")

    try:
        threshold = int(value)
    except ValueError:
        return 50

    return threshold if threshold >= 0 else 50


DEFAULT_INVENTORY_THRESHOLD: int = _load_default_inventory_threshold()
