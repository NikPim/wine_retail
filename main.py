from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends
import redis
from database import Base, Order as DBOrder, Wine as DBWine, WineReviewDB
from schema import Order, Wine
import psycopg2

# docker run --name postgres -e POSTGRES_PASSWORD=1111 -p 48162:5432 -d -e POSTGRES_DB=wine_store postgres
connection = psycopg2.connect(
    dbname='wine_store',
    user='postgres',
    password='1111',
    host='localhost',
    port='5432'
)
cur = connection.cursor()

# docker run --name some-redis -p 6379:6379 -d redis
redis_host = 'localhost'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port)
app = FastAPI()

def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()

DATABASE_URL = "postgresql://postgres:1111@localhost/wine_store"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


@app.get("/wine/{wine_id}")
def get_wine(wine_id: int, db: Session = Depends(get_db)):
    if r.exists(wine_id):
        return ('redis', r.hgetall(wine_id))

    db_wines = db.query(WineReviewDB).filter(WineReviewDB.id == wine_id).first()
    if not db_wines:
        raise HTTPException(status_code=404, detail="No wines in catalog")
    db_wines = db_wines.__dict__
    db_wines.pop('_sa_instance_state', None)
    for key, value in db_wines.items():
        if value is None:
            db_wines[key] = ""

    r.hmset(wine_id, db_wines)

    return ('postges', db_wines)


@app.post("/wine")
def add_wine(wine: Wine, db: Session = Depends(get_db)):
    db_wine =  DBWine(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return Wine(**db_wine.__dict__)


@app.get("/orders/{customer_id}", response_model=List[Order])
def read_orders(customer_id: int, db: Session = Depends(get_db)):
    # Query the database to retrieve orders and their associated items
    db_orders = db.query(DBOrder).filter(DBOrder.customer_id == customer_id).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found for this customer")
    # Serialize the SQLAlchemy models to Pydantic models
    orders = [db_order.__dict__ for db_order in db_orders]
    return orders
