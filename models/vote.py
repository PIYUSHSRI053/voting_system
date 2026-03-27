from pydantic import BaseModel
from typing import Optional

class VoteCreate(BaseModel):
    voter_id: str
    candidate_id: str
    proof_image: str

class VoteResponse(BaseModel):
    id: str
    voter_id: str
    candidate_id: str
    timestamp: str