from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends, Path
from tortoise.contrib.fastapi import register_tortoise
import tortoise.contrib.pydantic
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from schemas import FilmCreate, Film, GetCategoryFilms, GetCategory, FilmActor, FilmImage
from models import Films
import uvicorn
import logging
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # maybe should be rewritten
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_film_with_categories(film: Films) -> GetCategoryFilms:
    categories = await film.categories.all()
    cast = await film.cast.all()
    images = await film.image.all()
    return GetCategoryFilms(
        id=film.id,
        title=film.title,
        director=film.director,
        year=film.year,
        description=film.description,
        length=film.length,
        rating=film.rating,
        categories=[GetCategory.from_orm(category) for category in categories],
        cast=[FilmActor.from_orm(actor) for actor in cast],
        image=[FilmImage.from_orm(image) for image in images],
    )


@app.get("/films", response_model=List[GetCategoryFilms])
async def get_films():
    films = await Films.all().prefetch_related("categories", "cast", "image")
    return [await get_film_with_categories(film) for film in films]


@app.get("/films/search", response_model=List[GetCategoryFilms])
async def search_films(name: str):
    films = await Films.filter(title__icontains=name).prefetch_related("categories", "cast", "image")
    return [await get_film_with_categories(film) for film in films]


async def get_film(film_id: int):
    film = await Films.get_or_none(id=film_id).prefetch_related("categories")
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


async def create_film(film: FilmCreate):
    new_film = await Films.create(**film.dict())
    return new_film


async def delete_film(film_id: int):
    film = await Films.get_or_none(id=film_id)
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    await film.delete()
    return {"message": "Film deleted"}


@app.get("/films", response_model=List[Film])
async def read_films():
    return await get_films()


@app.get("/films/{film_id}", response_model=Film)
async def read_film(film_id: int):
    return await get_film(film_id)


@app.post("/films", response_model=Film)
async def create_film_endpoint(film: FilmCreate):
    return await create_film(film)


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_URL}/test"
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, lifespan='on', log_level="info")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
