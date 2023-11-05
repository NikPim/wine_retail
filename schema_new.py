from typing import List
from pydantic import BaseModel
from datetime import datetime

class WineBase(BaseModel):
    name: str
    vineyard: str
    varietal: str
    vintage: int
    price: float
    stock_quantity: int

class CustomerBase(BaseModel):
    name: str
    email: str


class OrderItemBase(BaseModel):
    order_id: int
    wine_id: int
    quantity: int
    price: float


class OrderBase(BaseModel):
    customer_id: int
    status: str
    order_date: datetime

class Order(OrderBase):
    id: int
    order_items: List[OrderItemBase] = []

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