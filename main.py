from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Membuat semua tabel di database secara otomatis
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="API untuk manajemen To-Do List (Proyek UTS Pemrograman Web Lanjutan)",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Selamat datang di To-Do List API Farel!"}

# ==========================
# ENDPOINT CRUD USER
# ==========================

@app.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    # Simpan user baru (Nanti password ini akan kita hash di fase JWT)
    new_user = models.User(email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users