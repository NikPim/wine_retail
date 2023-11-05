from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "postgresql://postgres:1111@localhost/wine_store"
engine = create_engine(DATABASE_URL)
# Create a session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()


# # Dependency to override the get_db dependency in the main app
# def override_get_db():
#     database = session()
#     yield database
#     database.close()


# app.dependency_overrides[get_db] = override_get_db


def test_create_item():
    response = client.post(
        "/wine/", json={"name": 'Wine test', "vineyard": "Wineyard test", "vintage": 1900, "stock_quantity": 100, "varietal":'test', "price": 1}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Wine test"
    assert data["price"] == 1
    assert "id" in data
