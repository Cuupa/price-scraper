from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    url: str
    current_price: str
    lowest_price: str
    currency: str
