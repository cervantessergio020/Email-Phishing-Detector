from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
import openapi
import re
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Optional

# Load environment variables
load_dotenv()

# MySQL database credentials
DATABASE_URL = "mysql+pymysql://admin:EmailProject1@phishingemailproject.cn0geogwil7k.us-east-2.rds.amazonaws.com/email_database"

# Create database engine
engine = create_engine(DATABASE_URL)

#interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Database Models
class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(255), nullable=False)
    emails = relationship("Email", back_populates="user")

class Email(Base):
    __tablename__ = 'Email'
    email_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    subject = Column(String(255), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    score = Column(Integer, nullable=True)
    has_attachment = Column(Boolean, default=False)
    issues = Column(Text, nullable=True)
    sender = Column(String(255), nullable=True)
    user = relationship("User", back_populates="emails")

class QRCode(Base):
    __tablename__ = 'QRCode'
    qrcode_id = Column(Integer, primary_key=True, autoincrement=True)
    attachment_link = Column(Text, nullable=False)

class EmailToQR(Base):
    __tablename__ = 'EmailToQR'
    email_id = Column(Integer, ForeignKey('Email.email_id'), primary_key=True)
    qrcode_id = Column(Integer, ForeignKey('QRCode.qrcode_id'), primary_key=True)

# Creates tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Enable CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Pydantic Models for Request Validation
class LoginRequest(BaseModel):
    username: str
    password: str

class EmailCreate(BaseModel):
    user_id: int
    subject: Optional[str] = None
    score: Optional[int] = None
    has_attachment: Optional[bool] = False
    issues: Optional[str] = None
    sender: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    user_password: str

# Email Score Endpoint
@app.get("/email/score")
def get_score(user_email: str, user_url: str):
    response = openapi.analyze_email(user_email, user_url)
    first_line = response.split("\n")[0]
    score_match = re.search(r'\d+', first_line)
    score = int(score_match.group()) if score_match else None
    return {"score": score}

# Login Endpoint (Now uses MySQL User table)
@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        #  If user exists, check password
        if not verify_password(user.password, existing_user.user_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "user": {"id": existing_user.user_id, "username": existing_user.username}}

    #  If user does not exist, register them automatically
    new_user = User(username=user.username, user_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered and logged in", "user": {"id": new_user.user_id, "username": new_user.username}}

# Create an Email Entry
@app.post("/emails/")
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    new_email = Email(
        user_id=email.user_id,
        subject=email.subject,
        score=email.score,
        has_attachment=email.has_attachment,
        issues=email.issues,
        sender=email.sender
    )
    db.add(new_email)
    db.commit() 
    db.refresh(new_email)
    return new_email

# Get Email by ID
@app.get("/emails/{email_id}")
def read_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.email_id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

# Get All Emails
@app.get("/emails/")
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Email).offset(skip).limit(limit).all()

# Get All Users
@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

