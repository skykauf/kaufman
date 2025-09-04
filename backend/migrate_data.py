#!/usr/bin/env python3
"""
Data migration script to import recipes from extracted_recipes.json into the database
"""
import json
import sys
import os
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models import Recipe

def load_recipes_from_json(file_path: str):
    """Load recipes from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def create_ingredients_text(ingredients):
    """Create searchable text from ingredients list"""
    if not ingredients:
        return ""
    
    text_parts = []
    for ingredient in ingredients:
        if isinstance(ingredient, dict) and 'item' in ingredient:
            item = ingredient['item']
            quantity = ingredient.get('quantity', '')
            unit = ingredient.get('unit', '')
            text_parts.append(f"{quantity} {unit} {item}".strip())
        elif isinstance(ingredient, str):
            text_parts.append(ingredient)
    
    return " | ".join(text_parts)

def migrate_recipes(db: Session, recipes_data):
    """Migrate recipes to database"""
    migrated_count = 0
    skipped_count = 0
    
    for recipe_data in recipes_data:
        # Skip recipes without names
        if not recipe_data.get('recipe_name'):
            skipped_count += 1
            continue
        
        # Check if recipe already exists
        existing = db.query(Recipe).filter(
            Recipe.recipe_name == recipe_data['recipe_name']
        ).first()
        
        if existing:
            print(f"Recipe '{recipe_data['recipe_name']}' already exists, skipping...")
            skipped_count += 1
            continue
        
        # Create ingredients text for search
        ingredients_text = create_ingredients_text(recipe_data.get('ingredients', []))
        
        # Create recipe object
        recipe = Recipe(
            recipe_name=recipe_data.get('recipe_name', ''),
            cuisine_type=recipe_data.get('cuisine_type'),
            difficulty=recipe_data.get('difficulty'),
            prep_time=recipe_data.get('prep_time'),
            cook_time=recipe_data.get('cook_time'),
            total_time=recipe_data.get('total_time'),
            servings=recipe_data.get('servings'),
            ingredients=recipe_data.get('ingredients', []),
            ingredients_text=ingredients_text,
            instructions=recipe_data.get('instructions', []),
            description=recipe_data.get('description'),
            notes=recipe_data.get('notes'),
            source=recipe_data.get('source', 'Mimi\'s Collection')
        )
        
        try:
            db.add(recipe)
            db.commit()
            migrated_count += 1
            print(f"Migrated: {recipe_data['recipe_name']}")
        except Exception as e:
            print(f"Error migrating recipe '{recipe_data['recipe_name']}': {e}")
            db.rollback()
            skipped_count += 1
    
    return migrated_count, skipped_count

def main():
    """Main migration function"""
    # Default path to recipes file
    recipes_file = "../extracted_recipes.json"
    
    if len(sys.argv) > 1:
        recipes_file = sys.argv[1]
    
    if not os.path.exists(recipes_file):
        print(f"Error: Recipes file '{recipes_file}' not found")
        sys.exit(1)
    
    print("Creating database tables...")
    create_tables()
    
    print(f"Loading recipes from {recipes_file}...")
    recipes_data = load_recipes_from_json(recipes_file)
    
    if not recipes_data:
        print("No recipes found to migrate")
        sys.exit(1)
    
    print(f"Found {len(recipes_data)} recipes to process")
    
    # Create database session
    db = SessionLocal()
    
    try:
        migrated_count, skipped_count = migrate_recipes(db, recipes_data)
        print(f"\nMigration complete!")
        print(f"Migrated: {migrated_count} recipes")
        print(f"Skipped: {skipped_count} recipes")
    finally:
        db.close()

if __name__ == "__main__":
    main()
