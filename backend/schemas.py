from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class IngredientItem(BaseModel):
    item: str
    quantity: Optional[str] = None
    unit: Optional[str] = None

class RecipeBase(BaseModel):
    recipe_name: str
    cuisine_type: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    servings: Optional[str] = None
    ingredients: Optional[List[IngredientItem]] = []
    instructions: Optional[List[str]] = []
    description: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    ingredients_text: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
