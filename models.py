from database import Base
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum, DateTime, ForeignKey, Text, DECIMAL, Boolean
from typing import Optional
from enum import Enum as PyEnum, List
from datetime import datetime


class StatusChoices(str, PyEnum):
        client = 'client'
        owner = 'owner'
        courier = 'courier'



class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.client)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  
    owner_store: Mapped[List['Store']] = relationship('Store', back_populates='owner',
                                                      cascade='all, delete-orphan')


class Category(Base):
      
      __tablename__ = 'category'

      id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
      category_name: Mapped[str] = mapped_column(String(32), unique=True)
      category_store: Mapped[List['Store']] = relationship(back_populates='category',
                                                           cascade='all, delete-orphan')


class Store(Base):
      
      __tablename__ = 'store'

      id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
      store_name: Mapped[str] = mapped_column(String(32))
      category_id: Mapped[int] = mapped_column(ForeignKey('category'))
      category: Mapped["Category"] = relationship('Category', back_populates='category_store')
      description: Mapped[str] = mapped_column(Text)
      store_image: Mapped[str] = mapped_column(String)
      address: Mapped[str] = mapped_column(String(64))
      owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile_id'))
      owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='owner_store')
      store_contacts: Mapped[List['Contact']] = relationship('Contact', back_populates='store', 
                                                             cascade='all, delete-orphan')
      products_store: Mapped[List['Product']] = relationship('Product', back_populates='store_product',
                                                              cascade='all, delete-orphan')
      combo_store: Mapped[List['Combo']] = relationship('Combo', back_populates='store_combo',
                                                              cascade='all, delete-orphan')

class Contact(Base):
      
      __tablename__ = 'contact'

      id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
      title: Mapped[str] = mapped_column(String, nullable=True)
      contact_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
      social_network: Mapped[Optional[str]] = mapped_column(String, nullable=True)
      store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
      store: Mapped['Store'] = relationship('Store', back_populates='store_contacts')



class Product(Base):

     __tablename__ = 'product'

     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
     product_name: Mapped[str] = mapped_column(String(32))
     description: Mapped[str] = mapped_column(Text)
     product_image: Mapped[str] = mapped_column(String)
     price: Mapped[float] = mapped_column(DECIMAL(10, 2))
     store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
     store_product: Mapped['Store'] = relationship('Store', back_populates='product_store') 


class Combo(Base):
      
      __tablename__ = 'combo'

      id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
      combo_name: Mapped[str] = mapped_column(String(32))
      is_combo: Mapped[bool] = mapped_column(Boolean)
      price: Mapped[float] = mapped_column(DECIMAL(10, 2))
      store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
      store: Mapped['Store'] = relationship('Store', back_populates='store_combo')



