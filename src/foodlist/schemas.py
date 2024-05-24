
from src.models import CustomModel
from typing import List

class Food(CustomModel):
    name: str
    calories: int
    tags: List[str]
    ingredients: List[str]