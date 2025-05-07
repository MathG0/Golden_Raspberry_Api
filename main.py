from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import csv
import os
from collections import defaultdict
from database import SessionLocal, Movie, Base, engine
from contextlib import asynccontextmanager
from pydantic import BaseModel, ConfigDict
from typing import List

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    load_data_from_csv(db)
    db.close()
    yield

app = FastAPI(lifespan=lifespan)

class MovieBase(BaseModel):
    title: str
    year: int
    winner: bool
    producer: str

class MovieResponse(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_data_from_csv(db: Session):
    if not os.path.exists("movies.csv"):
        print("Arquivo movies.csv não encontrado.")
        return
    
    db.query(Movie).delete()
    db.commit()

    try:
        with open("movies.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    db.add(Movie(
                        year=int(row["year"]),
                        title=row["title"],
                        producer=row["producer"],
                        winner=row["winner"].strip().lower() == "true"
                    ))
                except ValueError:
                    print(f"Erro ao processar linha: {row}")
        db.commit()
        print("Dados do CSV carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")

@app.get("/")
def home():
    return {"message": "API funcionando! Vá para /docs para ver a documentação."}

@app.get("/producers/intervals")
def get_producers_intervals(db: Session = Depends(get_db)):
    winners = db.query(Movie).filter(Movie.winner == True).order_by(Movie.year).all()

    producer_wins = defaultdict(list)
    for movie in winners:
        if movie.producer not in producer_wins:
            producer_wins[movie.producer] = []
        if movie.year not in producer_wins[movie.producer]:
            producer_wins[movie.producer].append(movie.year)

    intervals = []
    for producer, years in producer_wins.items():
        if len(years) > 1:
            for i in range(len(years) - 1):
                interval = years[i + 1] - years[i]
                intervals.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })

    if not intervals:
        return {"min": [], "max": []}

    min_interval = min(intervals, key=lambda x: x["interval"])["interval"]
    max_interval = max(intervals, key=lambda x: x["interval"])["interval"]

    min_intervals = [i for i in intervals if i["interval"] == min_interval]
    max_intervals = [i for i in intervals if i["interval"] == max_interval]

    return {"min": min_intervals, "max": max_intervals}

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()
