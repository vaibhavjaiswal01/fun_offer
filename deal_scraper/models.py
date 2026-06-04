from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ProductInfo:
    source_url: str
    resolved_url: str
    domain: str
    site_name: str
    title: str | None = None
    brand: str | None = None
    price: str | None = None
    currency: str | None = None
    image_url: str | None = None
    description: str | None = None
    availability: str | None = None
    rating: str | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
