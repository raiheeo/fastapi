from fastapi import FastAPI, Depends, HTTPE
from database import SessionLocal
from schema import *
from sqlalchemy.orm import Session
from typing import List, Dict
from fastapi import HTTPException
from models import *
from config import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, ACCES_TOKEN
from jose import jwt, JWTError
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


fludd_app = FastAPI(title='Fludd')

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

@fludd_app.post('/stpre/create')
async def store_create(store: StoreCreate, db: Session = Depends(get_db))
    Store(**store.dict())


@fludd_app.post('/store/create/')
async def store_create(store: StoreCreate, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@fludd_app.get('/store/', response_model=List[StoreSchema])
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()


@fludd_app.get('/store/{store_id}/', response_model=StoreSchema)
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Магазин не найден')
    return store_db

@fludd_app.put('/store/{store_id}', response_model=StoreSchema)
async def store_update(store_id: int, store: StoreSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Магазин не найден')
    

    for key, value in store.dict().items():
        setattr(store_db, key, value)
    
    db.commit()
    db.refresh(store_db)
    return store_db


raise HTTPException(status_code=404, detail="Магазин не найден")

for store_key, store_value in store.dict().items():
    setattr(store_db, store_key, store_value)

    db.add(store_db)
    db.commit()
    db.refresh(store.db)

@delivery_app.delete('/store/{store_id}/')
async def store_delete(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Магазин не найден')
    
    db.delete(store_db)
    db.commit()
    return {"message": "Магазин успешно удален"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)


@fludd_app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_db(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not password_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_user_from_db(username: str):
    return UserInDB(username=username, hashed_password="hashed_password")


token_blacklist = set()

def add_token_to_blacklist(token: str):
    token_blacklist.add(token)

def is_token_blacklisted(token: str):
    return token in token_blacklist

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already invalidated",
        )
    add_token_to_blacklist(token)
    return {"message": "Successfully logged out"}