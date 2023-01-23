"""Context class."""
from __future__ import annotations

from datetime import datetime

from .container import Container


class Context(Container):
    """Context class."""

    def __init__(self, **kwargs) -> Context:
        """Create a new Context instance."""
        super().__init__(**kwargs)
        self._container["timestamp"] = datetime.now().timestamp()
        self._container["date"] = datetime.now().strftime("%Y%m%d")
        self._container["iso_date"] = datetime.now().isoformat()
