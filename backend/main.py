from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
import shutil
from pathlib import Path

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

@app.post("/upload-recipe-photos")
async def upload_recipe_photos(
    folder_id: str = Form(...),
    front_photo: UploadFile = File(...),
    back_photo: UploadFile = File(...)
):
    """Upload front and back photos of a recipe card"""
    
    # Validate file types
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/heic", "image/heif"]
    
    if front_photo.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Front photo must be a valid image file")
    
    if back_photo.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Back photo must be a valid image file")
    
    # Validate file sizes (10MB max)
    max_size = 10 * 1024 * 1024  # 10MB
    
    front_content = await front_photo.read()
    back_content = await back_photo.read()
    
    if len(front_content) > max_size:
        raise HTTPException(status_code=400, detail="Front photo file size exceeds 10MB limit")
    
    if len(back_content) > max_size:
        raise HTTPException(status_code=400, detail="Back photo file size exceeds 10MB limit")
    
    try:
        # Create the upload directory path
        base_path = Path(__file__).parent.parent / "mimi_recipe_pictures" / folder_id
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Determine file extensions
        front_ext = ".jpg" if front_photo.content_type in ["image/jpeg", "image/jpg"] else \
                   ".png" if front_photo.content_type == "image/png" else \
                   ".heic"
        
        back_ext = ".jpg" if back_photo.content_type in ["image/jpeg", "image/jpg"] else \
                  ".png" if back_photo.content_type == "image/png" else \
                  ".heic"
        
        # Save files with proper names
        front_path = base_path / f"front{front_ext}"
        back_path = base_path / f"back{back_ext}"
        
        # Write files
        with open(front_path, "wb") as f:
            f.write(front_content)
        
        with open(back_path, "wb") as f:
            f.write(back_content)
        
        return {
            "message": "Photos uploaded successfully",
            "folder_id": folder_id,
            "front_photo": f"front{front_ext}",
            "back_photo": f"back{back_ext}",
            "upload_path": str(base_path)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photos: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
