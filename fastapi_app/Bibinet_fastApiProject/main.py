import json

from fastapi import FastAPI, Depends, Body
import psycopg2
from typing import List, Annotated, Optional
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
    print(dict_rows)
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
async def search_part_view(*,
                           coon=Depends(connection),
                           page: int = 1,
                           page_size: int = 10,
                           part_name: str = Body(embed=True),
                           mark_name: Annotated[Optional[str], Body()],
                           mark_list: Annotated[Optional[List[int]], Body()],
                           params: dict = Body(embed=True),
                           price_gte: float = Body(embed=True),
                           price_lte: float = Body(embed=True),
                           ):
    cur = coon.cursor()
    if mark_list not in [None, '', []]:
        cur.execute(f"SELECT part_app_part.mark_id_id, part_app_mark.name, part_app_mark.producer_country_name, "
                    f"part_app_part.model_id_id, part_app_model.name, part_app_part.name, "
                    f"part_app_part.price, part_app_part.json_data, part_app_part.is_visible FROM part_app_part "
                    f"INNER JOIN part_app_mark ON (part_app_part.mark_id_id = part_app_mark.id)"
                    f"INNER JOIN part_app_model ON (part_app_part.model_id_id = part_app_model.id) WHERE"
                    f"(part_app_part.json_data @> '{json.dumps(params)}' AND part_app_part.mark_id_id IN "
                    f"{tuple(mark_list)} AND "
                    f"part_app_part.name::text LIKE '{part_name}' AND part_app_part.price >= {price_gte} "
                    f"AND part_app_part.price <= {price_lte})")
    elif mark_name not in [None, '']:
        cur.execute(f"SELECT part_app_part.mark_id_id, part_app_mark.name, part_app_mark.producer_country_name, "
                    f"part_app_part.model_id_id, part_app_model.name, part_app_part.name, "
                    f"part_app_part.price, part_app_part.json_data, part_app_part.is_visible FROM part_app_part "
                    f"INNER JOIN part_app_mark ON (part_app_part.mark_id_id = part_app_mark.id)"
                    f"INNER JOIN part_app_model ON (part_app_part.model_id_id = part_app_model.id) WHERE "
                    f"(part_app_part.json_data @> '{json.dumps(params)}' AND part_app_mark.name::text LIKE '{mark_name}' AND "
                    f"part_app_part.name::text LIKE '{part_name}' AND part_app_part.price >= {price_gte} "
                    f"AND part_app_part.price <= {price_lte})")
    dict_rows = [dict(zip(["mark_id", "mark_name", "mark_producer_country_name", "model_id", "model_name",
                           "part_name", "price", "json_data", "is_visible"], list(row))) for row in cur.fetchall()]

    offset_min = page_size * (page - 1)
    offset_max = page_size * page
    return dict_rows[offset_min:offset_max] + [{"page": page, "count": len(dict_rows),
                                                "summ": sum([dict_rows[i]["price"] for i in range(len(dict_rows))])}]
