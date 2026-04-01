from pydantic import BaseModel


# ========== Pydantic модели ==========
class ItemCreate(BaseModel):
    name: str
    price: float


class ItemResponse(ItemCreate):
    id: int
