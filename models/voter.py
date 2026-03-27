from pydantic import BaseModel, EmailStr
from typing import Optional

class VoterCreate(BaseModel):
    name: str
    email: str
    phone: str
    national_id: str
    password: str
    address: str
    face_encoding: bytes
    photo_path: str

class VoterLogin(BaseModel):
    email: str
    password: str

class Vote(BaseModel):
    voter_id: str
    candidate_id: str
    