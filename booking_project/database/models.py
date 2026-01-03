from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Enum, Date, DateTime, ForeignKey, Text
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(PyEnum):
    client = 'client'
    owner = 'owner'

class RoomTypeChoices(PyEnum):
    Люкс = 'Люкс'
    Полулюкс = 'Полулюкс'
    Семейный = 'Семейный'
    Эконом = 'Эконом'
    Одноместный = 'Одноместный'

class RoomStatusChoices(PyEnum):
    Занят = 'Занят'
    Забронирован = 'Забронирован'
    Свободен = 'Свободен'


class Country(Base):
    __tablename__ = 'booking_country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_image: Mapped[str] = mapped_column(String)
    country_name: Mapped[str] = mapped_column(String, unique=True)

    users: Mapped[List['UserProfile']] = relationship('UserProfile',
                                                      back_populates='country',
                                                      cascade='all, delete-orphan')
    country: Mapped[List['City']] = relationship('City',
                                                 back_populates='countries',
                                                 cascade='all, delete-orphan')
    country_hotel: Mapped[List['Hotel']] = relationship('Hotel',
                                                        back_populates='hotel_country',
                                                        cascade='all, delete-orphan')


class UserProfile(Base):
    __tablename__ = 'booking_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    registered_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    country_id: Mapped[int] = mapped_column(ForeignKey('booking_country.id'))

    country: Mapped[Country] = relationship('Country', back_populates='users')
    owner_hotel: Mapped[List['Hotel']] = relationship('Hotel',
                                                      back_populates='owner',
                                                      cascade='all, delete-orphan')
    review_user: Mapped[List['Review']] = relationship('Review',
                                                       back_populates='user_review',
                                                       cascade='all, delete-orphan')
    booking_user: Mapped[List['Booking']] = relationship('Booking',
                                                         back_populates='user_booking',
                                                         cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken',
                                                            back_populates='token_user',
                                                            cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('booking_profile.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')


class City(Base):
    __tablename__ = 'booking_city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_image: Mapped[str] = mapped_column(String)
    city_name: Mapped[str] = mapped_column(String, unique=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('booking_country.id'))

    countries: Mapped[Country] = relationship(Country, back_populates='country')
    city_hotel: Mapped[List['Hotel']] = relationship('Hotel',
                                                     back_populates='hotel_city',
                                                     cascade='all, delete-orphan')


class Service(Base):
    __tablename__ = 'booking_service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_image: Mapped[str] = mapped_column(String)
    service_name: Mapped[str] = mapped_column(String, unique=True)

    service_hotel: Mapped[List['Hotel']] = relationship('Hotel',
                                                        back_populates='hotel_service',
                                                        cascade='all, delete-orphan')


class Hotel(Base):
    __tablename__ = 'booking_hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[int] = mapped_column(Integer)
    hotel_stars: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    country_id: Mapped[int] = mapped_column(ForeignKey('booking_country.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('booking_city.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('booking_service.id'))
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('booking_profile.id'), nullable=True)

    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='owner_hotel')
    hotel_service: Mapped[Service] = relationship(Service, back_populates='service_hotel')
    hotel_city: Mapped[City] = relationship(City, back_populates='city_hotel')
    hotel_country: Mapped[Country] = relationship(Country, back_populates='country_hotel')
    images: Mapped[List['HotelImage']] = relationship('HotelImage',
                                                      back_populates='image_hotel',
                                                      cascade='all, delete-orphan')
    room_hotel: Mapped[List['Room']] = relationship('Room',
                                                    back_populates='hotel_room',
                                                    cascade='all, delete-orphan')
    images_room: Mapped[List['RoomImage']] = relationship('RoomImage',
                                                          back_populates='image_room',
                                                          cascade='all, delete-orphan')
    review_hotel: Mapped[List['Review']] = relationship('Review',
                                                        back_populates='hotel_review',
                                                        cascade='all, delete-orphan')
    booking_hotel: Mapped[List['Booking']] = relationship('Booking',
                                                          back_populates='hotel_booking',
                                                          cascade='all, delete-orphan')


class HotelImage(Base):
    __tablename__ = 'booking_hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_image: Mapped[str] = mapped_column(String)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('booking_hotel.id'))

    image_hotel: Mapped[Hotel] = relationship(Hotel, back_populates='images')


class Room(Base):
    __tablename__ = 'booking_room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices))
    room_status: Mapped[RoomStatusChoices] = mapped_column(Enum(RoomStatusChoices))
    description: Mapped[str] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('booking_hotel.id'))

    hotel_room: Mapped[Hotel] = relationship(Hotel, back_populates='room_hotel')
    booking_room: Mapped[List['Booking']] = relationship('Booking',
                                                         back_populates='room_booking',
                                                         cascade='all, delete-orphan')


class RoomImage(Base):
    __tablename__ = 'booking_room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_image: Mapped[str] = mapped_column(String)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('booking_hotel.id'))

    image_room: Mapped[Hotel] = relationship(Hotel, back_populates='images_room')


class Review(Base):
    __tablename__ = 'booking_review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_add: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('booking_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('booking_hotel.id'))

    user_review: Mapped[UserProfile] = relationship(UserProfile, back_populates='review_user')
    hotel_review: Mapped[Hotel] = relationship(Hotel, back_populates='review_hotel')


class Booking(Base):
    __tablename__ = 'booking_booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(ForeignKey('booking_profile.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('booking_hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('booking_room.id'))

    user_booking: Mapped[UserProfile] = relationship(UserProfile, back_populates='booking_user')
    hotel_booking: Mapped[Hotel] = relationship(Hotel, back_populates='booking_hotel')
    room_booking: Mapped[Room] = relationship(Room, back_populates='booking_room')
