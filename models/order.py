"""
`Order` model to represent choices of the user 
upon which meal will be generated.
"""

from pydantic import BaseModel
from typing import List, Optional


class Order(BaseModel):
    """Order object."""

    q: str
    cuisineType: Optional[List[str]] = []
    mealType: Optional[List[str]] = []
    diet: Optional[List[str]] = []
    health: Optional[List[str]] = []
