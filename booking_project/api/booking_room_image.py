from fastapi import APIRouter, Depends, HTTPException
from booking_project.database.models import RoomImage
from booking_project.database.schema import RoomImageInputSchema, RoomImageOutSchema
from booking_project.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

room_image_router = APIRouter(prefix='/room_image', tags=['RoomImages'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_image_router.post('/', response_model=RoomImageOutSchema)
async def create_room_image(room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
     room_image_db = RoomImage(**room_image.dict())
     db.add(room_image_db)
     db.commit()
     db.refresh(room_image)
     return room_image_db


@room_image_router.get('/', response_model=List[RoomImageOutSchema])
async def list_room_image(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()


@room_image_router.get('/{room_image_id}/', response_model=RoomImageOutSchema)
async def detail_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return room_image_db


@room_image_router.put('/{room_image_id}/', response_model=dict)
async def update_room_image(room_image_id: int, room_image: RoomImageInputSchema,
                         db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for room_image_key, room_image_value in room_image.dict().items():
            setattr(room_image_db, room_image_key, room_image_value)

    db.commit()
    db.refresh(room_image_db)
    return {'massage': 'Комнатанын суроту озгорулду'}


@room_image_router.delete('/{room_image_id}/', response_model=dict)
async def delete_room_image(room_image_id: int, db:  Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(room_image_db)
    db.commit()
    return {'massage': 'Комнатанын суроту удалить болду'}
