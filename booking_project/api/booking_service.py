from fastapi import APIRouter, Depends, HTTPException
from booking_project.database.models import Service
from booking_project.database.schema import ServiceInputSchema, ServiceOutSchema
from booking_project.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

service_router = APIRouter(prefix='/services', tags=['Services'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@service_router.post('/', response_model=ServiceOutSchema)
async def create_service(service: ServiceInputSchema, db: Session = Depends(get_db)):
     service_db = Service(**service.dict())
     db.add(service_db)
     db.commit()
     db.refresh(service_db)
     return service_db


@service_router.get('/', response_model=List[ServiceOutSchema])
async def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@service_router.get('/{service_id}/', response_model=ServiceOutSchema)
async def detail_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return service_db


@service_router.put('/{service_id}/', response_model=dict)
async def update_service(service_id: int, service: ServiceInputSchema,
                         db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for service_key, service_value in service.dict().items():
        setattr(service_db, service_key, service_value)

    db.commit()
    db.refresh(service_db)
    return {'massage': 'Сервис озгорулду'}


@service_router.delete('/{service_id}/', response_model=dict)
async def delete_service(service_id: int, db:  Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()
    if not service_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(service_db)
    db.commit()
    return {'massage': 'Сервис удалить болду'}