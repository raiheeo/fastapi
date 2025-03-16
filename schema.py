from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Enum
from pydantic import BaseModel, EmailStr

class StatusChoices(str, Enum):
    client = "client"
    admin = "admin"
    manager = "manager" 

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    age: Optional[int] = None
    status: StatusChoices = StatusChoices.client

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    date_registered: datetime

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class StoreBase(BaseModel):
    store_name: str
    category_id: int
    description: str
    store_image: str
    address: str
    owner_id: int

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    title: Optional[str] = None
    contact_number: Optional[str] = None
    social_network: Optional[str] = None
    store_id: int

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    product_name: str
    description: str
    product_image: str
    price: float
    store_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ComboBase(BaseModel):
    combo_name: str
    is_combo: bool
    price: float
    store_id: int

class ComboCreate(ComboBase):
    pass

class Combo(ComboBase):
    id: int

    class Config:
        orm_mode = True