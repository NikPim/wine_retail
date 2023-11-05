from pydantic import BaseModel
from typing import List
from datetime import datetime

class WineBase(BaseModel):
    name: str
    vineyard: str
    varietal: str
    vintage: int
    price: float
    stock_quantity: int
    class Config:
        orm_mode = True
        from_attributes = True
        from_orm = True

class WineCreate(WineBase):
    pass

class Wine(WineBase):
    id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    order_id: int
    wine_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
        from_orm = True

class OrderBase(BaseModel):
    customer_id: int
    status: str
    order_date: datetime

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_items: List[OrderItem] = []

    class Config:
        orm_mode = True
        from_attributes = True
        from_orm = True

class WineReviewBase(BaseModel):
    id: int
    country: str
    description: str
    designation: str
    price: str
    province: str
    region_1: str
    region_2: str
    variety: str
    points: str
    winery: str