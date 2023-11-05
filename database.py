from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Type

Base = declarative_base()

class NotFoundError(Exception):
    pass


class Wine(Base):
    __tablename__ = "wines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    vineyard = Column(String)
    varietal = Column(String)
    vintage = Column(Integer)
    price = Column(Float)
    stock_quantity = Column(Integer)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    # Add fields for address, billing info, etc.
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String)  # In progress, completed, etc.
    order_date = Column(DateTime)
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    wine_id = Column(Integer, ForeignKey("wines.id"))
    quantity = Column(Integer)
    price = Column(Float)
    order = relationship("Order", back_populates="order_items")
    wine = relationship("Wine")

class WineReviewDB(Base):
    __tablename__ = "wine_reviews"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    designation = Column(String)
    price = Column(String)
    province = Column(String)
    region_1 = Column(String)
    region_2 = Column(String)
    variety = Column(String, nullable=False)
    points = Column(String, nullable=False)
    winery = Column(String)

def db_find_item(item_id: int, session: Session, item_type: Type):
    db_item = session.query(item_type).filter(item_type.id == item_id).first()
    if not db_item:
        raise NotFoundError(f"{item_type.__name__} not found")
    return db_item
