from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import ItemCreate, ItemResponse


router = APIRouter(tags=['api'])


@router.post("/items", response_model=ItemResponse, summary="Добавление нового товара.")
async def create_item(item: ItemCreate, db=Depends(get_db)):
    """Добавить новый товар."""
    cursor = await db.execute(
        "INSERT INTO items (name, price) VALUES (?, ?)",
        (item.name, item.price)
    )
    await db.commit()
    item_id = cursor.lastrowid
    return ItemResponse(id=item_id, name=item.name, price=item.price)


@router.get("/items", response_model=List[ItemResponse], summary="Получение списка товаров.")
async def list_items(db=Depends(get_db)):
    """Получить список всех товаров."""
    cursor = await db.execute("SELECT id, name, price FROM items")
    rows = await cursor.fetchall()
    return [ItemResponse(id=row[0], name=row[1], price=row[2]) for row in rows]


@router.get("/items/{item_id}", response_model=ItemResponse, summary="Получение товара по ID.")
async def get_item(item_id: int, db=Depends(get_db)):
    """Получить товар по ID."""
    cursor = await db.execute(
        "SELECT id, name, price FROM items WHERE id = ?",
        (item_id,)
    )
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Товар не найден.")
    return ItemResponse(id=row[0], name=row[1], price=row[2])


@router.put("/items/{item_id}", response_model=ItemResponse, summary="Обновление информации о товаре.")
async def update_item(item_id: int, item: ItemCreate, db=Depends(get_db)):
    """Обновить существующий товар."""
    cursor = await db.execute(
        "UPDATE items SET name = ?, price = ? WHERE id = ?",
        (item.name, item.price, item_id)
    )
    await db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(id=item_id, name=item.name, price=item.price)


@router.delete("/items/{item_id}", summary="Удаление товара.")
async def delete_item(item_id: int, db=Depends(get_db)):
    """Удалить товар."""
    cursor = await db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    await db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}
