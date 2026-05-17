import json
import os


_DEFAULTS = {
    "sim_steps":      200,
    "base_lambda":    0.30,
    "rush_hour":      False,
    "cars_per_green": 1,
}


def load_config(path: str = "data/input_config.json") -> dict:
    """Load simulation config from JSON, falling back to defaults."""
    if not os.path.exists(path):
        print(f"[config] '{path}' not found – using defaults.")
        return dict(_DEFAULTS)
    with open(path) as f:
        cfg = json.load(f)
    merged = {**_DEFAULTS, **cfg}   # JSON values override defaults
    return merged