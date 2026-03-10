"""Infrastructure state loading and validation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateValidationError(ValueError):
    """Raised when input state is malformed."""


def load_state(path: str | Path) -> dict[str, Any]:
    """Load infrastructure state JSON from disk and validate its shape."""

    with Path(path).open("r", encoding="utf-8") as infile:
        data = json.load(infile)

    if not isinstance(data, dict):
        raise StateValidationError("Infrastructure state must be a JSON object")

    return data
