from fastapi import APIRouter, Depends, HTTPException
from booking_project.database.models import Booking
from booking_project.database.schema import BookingInputSchema, BookingOutSchema
from booking_project.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.post('/', response_model=BookingOutSchema)
async def create_booking(booking: BookingInputSchema, db: Session = Depends(get_db)):
     booking_db = Booking(**booking.dict())
     db.add(booking_db)
     db.commit()
     db.refresh(booking_db)
     return booking_db


@booking_router.get('/', response_model=List[BookingOutSchema])
async def list_booking(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@booking_router.get('/{booking_id}/', response_model=BookingInputSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return booking_db


@booking_router.put('/{booking_id}/', response_model=dict)
async def update_booking(booking_id: int, booking: BookingInputSchema,
                         db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for booking_key, booking_value in booking.dict().items():
            setattr(booking_db, booking_key, booking_value)

    db.commit()
    db.refresh(booking_db)
    return {'massage': 'Бронь озгорулду'}


@booking_router.delete('/{booking_id}/', response_model=dict)
async def delete_booking(booking_id: int, db:  Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(booking_db)
    db.commit()
    return {'massage': 'Бронь удалить болду'}
