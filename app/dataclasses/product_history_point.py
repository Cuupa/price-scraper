from dataclasses import dataclass


@dataclass
class ProductHistoryPoint:
    id: int
    name: str
    url: str
    price: str
    currency: str
    date: str
