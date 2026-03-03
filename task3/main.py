import os
from typing import List

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

from my_selenium import get_data_from_web

app = FastAPI()
load_dotenv()
CONNECT_TO_DB = os.getenv("CONNECT_TO_DB")

engine = create_engine(CONNECT_TO_DB)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    availability = Column(String)
    link = Column(String)

class BookResponse(BaseModel):
    id: int
    name: str
    availability : str
    price : str
    link : str
    model_config = ConfigDict(from_attributes=True)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы БД созданы/проверены")

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/parse",tags=["Запуск selenium"])
def parse(db: Session = Depends(get_db)):

    try:
        data = get_data_from_web()

        db.bulk_insert_mappings(Book,data)
        db.commit()
        return {"success": True, "Error": None}
    except Exception as e:
        db.rollback()
        return {"success": False, "Error": str(e)}

@app.get("/get_data", tags=["Получить всю информацию"], response_model=List[BookResponse])
def get_data_from_db(db: Session = Depends(get_db)):

    try:
        data = db.query(Book).all()
        # print(data[0].keys())
        return data
    except Exception as e:
        return {"success": False, "Error": str(e)}

@app.get("/clear_tables", tags=["Пересоздание таблицы"])
def reset_database():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"success": True, "Error": None}
    except Exception as e:
        return {"success": False, "Error": str(e)}

@app.get("/clear_data", tags=["Очистка данных"])
def clear_data():
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("""
                    DO $$ DECLARE
                        r RECORD;
                    BEGIN
                        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                            EXECUTE 'TRUNCATE TABLE public.' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                        END LOOP;
                    END $$;
                """))
        return {"success": True, "Error": None}
    except Exception as e:
        return {"success": False, "Error": str(e)}
