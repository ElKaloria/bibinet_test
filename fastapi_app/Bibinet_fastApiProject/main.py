from fastapi import FastAPI, Depends
import psycopg2
from typing import List, Tuple
from schemas import *

app = FastAPI()


def connection():
    return psycopg2.connect(
        host="db",
        port="5432",
        database="BibinetDB",
        user="postgres",
        password="postgres123"
    )


@app.get("/mark", response_model=List[Mark])
async def mark_view(coon=Depends(connection), page: int = 1, page_size: int = 10):
    cur = coon.cursor()
    cur.execute("SELECT * FROM part_app_mark")
    dict_rows = [dict(zip(Mark.__fields__.keys(), list(row))) for row in cur.fetchall()]
    offset_min = page_size * (page - 1)
    offset_max = page_size * page
    return dict_rows[offset_min:offset_max] + [{"page": page}]


@app.get("/model")
async def mark_view(coon=Depends(connection), page: int = 1, page_size: int = 10):
    cur = coon.cursor()
    cur.execute("SELECT part_app_model.id, part_app_model.name, part_app_mark.id, part_app_mark.name, "
                "part_app_mark.producer_country_name, part_app_mark.is_visible, part_app_model.is_visible"
                " FROM part_app_model INNER JOIN part_app_mark ON part_app_model.mark_id_id = part_app_mark.id")
    dict_rows = [dict(zip(["id", "name", "mark_id", "mark_name", "producer_country_name", "mark_is_visible",
                           "model_is_visible"], list(row))) for row in cur.fetchall()]
    offset_min = page_size * (page - 1)
    offset_max = page_size * page
    return dict_rows[offset_min:offset_max] + [{"page": page}]


@app.post("/search")
async def search_part_view(coon=Depends(connection), page: int = 1, page_size: int = 10, name: str = ""):
    pass
