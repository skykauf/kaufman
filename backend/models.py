from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String(255), nullable=False, index=True)
    cuisine_type = Column(String(100), index=True)
    difficulty = Column(String(20), index=True)
    prep_time = Column(String(50))
    cook_time = Column(String(50))
    total_time = Column(String(50))
    servings = Column(String(20))
    
    # Store ingredients as JSON array and searchable text
    ingredients = Column(JSON)
    ingredients_text = Column(Text)  # For full-text search
    
    # Store instructions as JSON array
    instructions = Column(JSON)
    
    # Additional fields
    description = Column(Text)
    notes = Column(Text)
    source = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.recipe_name}')>"
