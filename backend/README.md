# Mimi's Recipe API Backend

A FastAPI backend for the recipe collection application with PostgreSQL database support.

## Features

- **FastAPI** web framework with automatic API documentation
- **PostgreSQL** database with SQLAlchemy ORM
- **Recipe Management** - CRUD operations for recipes
- **Search & Filtering** - Search by name, ingredients, cuisine, difficulty
- **Railway Deployment** ready configuration

## API Endpoints

- `GET /` - API root
- `GET /health` - Health check
- `GET /recipes` - Get recipes with optional filtering
- `GET /recipes/{recipe_id}` - Get specific recipe
- `POST /recipes` - Create new recipe
- `GET /cuisines` - Get available cuisine types
- `GET /stats` - Get recipe statistics

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Create database tables:
```bash
python -c "from database import create_tables; create_tables()"
```

4. Migrate existing recipe data:
```bash
python migrate_data.py
```

5. Run the server:
```bash
uvicorn main:app --reload
```

### Railway Deployment

1. **Deploy PostgreSQL Database:**
   - Create new project on Railway
   - Add PostgreSQL service
   - Note the connection details

2. **Deploy FastAPI Backend:**
   - Connect your GitHub repository
   - Set `DATABASE_URL` environment variable from PostgreSQL service
   - Railway will automatically detect and deploy using `railway.json`

3. **Migrate Data:**
   - After deployment, run the migration script:
   ```bash
   python migrate_data.py
   ```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `DEBUG` - Debug mode (development only)
- `ENVIRONMENT` - Environment name

## Database Schema

The `recipes` table includes:
- Basic info: name, cuisine, difficulty, timing
- Ingredients: JSON array + searchable text field
- Instructions: JSON array
- Metadata: timestamps, source, notes

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
