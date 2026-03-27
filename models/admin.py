from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class Candidate(BaseModel):
    name: str
    party: str
    description: str