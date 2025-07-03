from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# 👇 Import JWT functions and current_user dependency from your auth module
from auth import authenticate_user, create_access_token, get_current_user

# ----------------------------
# ENVIRONMENT CONFIG
# ----------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# ----------------------------
# DATABASE SETUP
# ----------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# FASTAPI APP
# ----------------------------
app = FastAPI()

# ----------------------------
# LOGIN ENDPOINT FOR JWT
# ----------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# ----------------------------
# PROTECTED MOVIE ENDPOINTS
# ----------------------------
@app.get("/movies")
def get_movies(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = db.execute(text("SELECT * FROM movies.movies")).fetchall()
    return [dict(row._mapping) for row in result]

@app.get("/movies/{movie_id}")
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = db.execute(
        text("SELECT * FROM movies.movies WHERE movie_id = :id"),
        {"id": movie_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return dict(result._mapping)

@app.post("/movies")
def create_movie(
    movie: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
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
    result = db.execute(query, movie)
    db.commit()
    return {"movie_id": result.fetchone()[0]}

@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    movie: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    movie["movie_id"] = movie_id
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
    result = db.execute(query, movie)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie updated"}

@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = text("DELETE FROM movies.movies WHERE movie_id = :id")
    result = db.execute(query, {"id": movie_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted"}
