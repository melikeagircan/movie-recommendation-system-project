# Movie Recommendation System

A Netflix-like movie recommendation system built with FastAPI, PostgreSQL, and K-means clustering.

## Features

- User authentication and management
- Movie catalog management
- Personalized movie recommendations using K-means clustering
- PostgreSQL database with Alembic migrations
- RESTful API with FastAPI

## Project Structure

```
movie_recommender/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configurations
│   ├── db/            # Database configurations
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
├── migrations/        # Database migrations
└── tests/            # Test files
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

## Testing

Run tests with:
```bash
pytest
```

## License

MIT 