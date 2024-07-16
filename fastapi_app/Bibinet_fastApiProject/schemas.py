from pydantic import BaseModel


class Mark(BaseModel):
    id: int
    name: str
    producer_country_name: str
    is_visible: bool


class Model(BaseModel):
    id: int
    name: str
    mark_id: Mark
    is_visible: bool


class Part(BaseModel):
    id: int
    name: str
    mark_id: Mark
    model_id: Model
    price: float
    json_data: dict
    is_visible: bool

