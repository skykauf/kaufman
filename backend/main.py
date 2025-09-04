from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from config import settings
from database import get_db
from models import Recipe as RecipeModel
from schemas import Recipe, RecipeCreate

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Mimi's Recipe API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/recipes", response_model=List[Recipe])
async def get_recipes(
    search: Optional[str] = Query(None, description="Search in recipe name and ingredients"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    skip: int = Query(0, ge=0, description="Number of recipes to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of recipes to return"),
    db: Session = Depends(get_db)
):
    """Get recipes with optional filtering"""
    query = db.query(RecipeModel)
    
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            RecipeModel.recipe_name.ilike(search_term) |
            RecipeModel.ingredients_text.ilike(search_term)
        )
    
    if cuisine_type:
        query = query.filter(RecipeModel.cuisine_type == cuisine_type)
    
    if difficulty:
        query = query.filter(RecipeModel.difficulty == difficulty)
    
    recipes = query.offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    db_recipe = RecipeModel(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.get("/cuisines")
async def get_cuisines(db: Session = Depends(get_db)):
    """Get all available cuisine types"""
    cuisines = db.query(RecipeModel.cuisine_type).filter(
        RecipeModel.cuisine_type.isnot(None),
        RecipeModel.cuisine_type != 'unknown'
    ).distinct().all()
    return [{"title": cuisine[0], "value": cuisine[0]} for cuisine in cuisines]

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get recipe statistics"""
    total_recipes = db.query(RecipeModel).count()
    total_cuisines = db.query(RecipeModel.cuisine_type).filter(
        RecipeModel.cuisine_type.isnot(None),
        RecipeModel.cuisine_type != 'unknown'
    ).distinct().count()
    
    return {
        "total_recipes": total_recipes,
        "total_cuisines": total_cuisines
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
