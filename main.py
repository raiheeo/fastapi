from fastapi import FastAPI, Depends, HTTPE
from database import SessionLocal
from schema import *
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException


fludd_app = FastAPI(title='Fludd')

@fludd_app.get("/")
async def root():
    return {"message:" "Hello World"}


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@fludd_app.post('category/create/')
async def category_create(category: Category, db: Session = Depends(get_db)):
    category_db = Category(category_name=category.category_name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@fludd_app.get('/category/', response_model=List[Category])
async def category_list(db: Session = Depends(get_db)):
    return db.query(Category).all() 


@fludd_app.get('/category/{category_id}', response_model=Category)
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')
    return category


@fludd_app.put('/category/{category_id}', response_model=CategorySchema)
async def category_update(category_id: int, category: CategorySchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Category not found')
    category_db.category_name = category.category_name
    db.add(category_db)
    db.commit()
    db.refresh(category_db) 
    return category_db


@fludd_app.delete('/category/{category_id}')
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category_db)
    db.commit()

    return {'message': 'This category is deleted'}