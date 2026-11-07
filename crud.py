"""Movies REST API: JWT-protected CRUD endpoints backed by PostgreSQL."""
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from auth import authenticate_user, create_access_token, get_current_user

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# REQUEST MODELS (input validation)
# ----------------------------
class MovieIn(BaseModel):
    movie_title: str = Field(min_length=1, max_length=255)
    movie_description: str | None = Field(default=None, max_length=1000)
    release_year: int | None = Field(default=None, ge=1880, le=2100)
    runtime_minutes: int | None = Field(default=None, ge=1, le=1000)
    rating: float | None = Field(default=None, ge=0, le=10)
    votes: int | None = Field(default=None, ge=0)
    revenue_millions: float | None = Field(default=None, ge=0)
    metascore: int | None = Field(default=None, ge=0, le=100)


app = FastAPI(title="Movies API")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Unauthenticated check that the API and database are up (for Docker and monitoring)."""
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


# ----------------------------
# LOGIN ENDPOINT FOR JWT
# ----------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


# ----------------------------
# PROTECTED MOVIE ENDPOINTS
# ----------------------------
@app.get("/movies")
def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = db.execute(
        text("SELECT * FROM movies.movies ORDER BY movie_id LIMIT :limit OFFSET :skip"),
        {"limit": limit, "skip": skip},
    ).fetchall()
    return [dict(row._mapping) for row in result]


@app.get("/movies/{movie_id}")
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = db.execute(
        text("SELECT * FROM movies.movies WHERE movie_id = :id"), {"id": movie_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return dict(result._mapping)


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieIn,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = text("""
        INSERT INTO movies.movies (
            movie_title, movie_description, release_year,
            runtime_minutes, rating, votes, revenue_millions, metascore
        ) VALUES (
            :movie_title, :movie_description, :release_year,
            :runtime_minutes, :rating, :votes, :revenue_millions, :metascore
        ) RETURNING movie_id
    """)
    try:
        movie_id = db.execute(query, movie.model_dump()).scalar_one()
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A movie with this title and year already exists")
    return {"movie_id": movie_id}


@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    movie: MovieIn,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    query = text("""
        UPDATE movies.movies SET
            movie_title = :movie_title,
            movie_description = :movie_description,
            release_year = :release_year,
            runtime_minutes = :runtime_minutes,
            rating = :rating,
            votes = :votes,
            revenue_millions = :revenue_millions,
            metascore = :metascore
        WHERE movie_id = :movie_id
    """)
    try:
        result = db.execute(query, {**movie.model_dump(), "movie_id": movie_id})
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A movie with this title and year already exists")
    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(status_code=404, detail="Movie not found")
    db.commit()
    return {"message": "Movie updated"}


@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = db.execute(text("DELETE FROM movies.movies WHERE movie_id = :id"), {"id": movie_id})
    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(status_code=404, detail="Movie not found")
    db.commit()
    return {"message": "Movie deleted"}
