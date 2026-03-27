import face_recognition
import numpy as np
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config.settings import Settings
from datetime import datetime
import cv2
import os

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(Settings.MONGO_URI)
        self.db = self.client[Settings.DB_NAME]
        
        self.voters = self.db.voters
        self.votes = self.db.votes
        self.candidates = self.db.candidates
        self.admins = self.db.admins
        
        self._create_indexes()
        self._ensure_demo_data()
    
    def _create_indexes(self):
        self.voters.create_index("email", unique=True)
        self.voters.create_index("phone", unique=True)
        self.voters.create_index("national_id", unique=True)
        self.votes.create_index("voter_id", unique=True)
    
    def _ensure_demo_data(self):
        """Add demo candidates if none exist"""
        if self.candidates.count_documents({}) == 0:
            demo_candidates = [
                {"name": "Candidate A", "party": "Party A", "description": "Development Focus"},
                {"name": "Candidate B", "party": "Party B", "description": "Education Focus"},
                {"name": "Candidate C", "party": "Party C", "description": "Healthcare Focus"}
            ]
            self.candidates.insert_many(demo_candidates)
    
    def register_voter(self, data):
        try:
            data['registered_at'] = datetime.now()
            data['status'] = 'pending'
            data['has_voted'] = False
            result = self.voters.insert_one(data)
            return str(result.inserted_id)
        except DuplicateKeyError as e:
            raise ValueError(f"Duplicate: {str(e)}")
    
    def login_voter(self, email, password):
        voter = self.voters.find_one({
            "email": email,
            "password": password,  # In production, use hash
            "status": "approved"
        })
        return voter
    
    def verify_face(self, voter_id, live_frame):
        voter = self.voters.find_one({"_id": voter_id})
        if not voter:
            return False
        
        stored_encoding = np.frombuffer(voter['face_encoding'])
        locations = face_recognition.face_locations(live_frame)
        
        if locations:
            live_encoding = face_recognition.face_encodings(live_frame, locations)[0]
            return face_recognition.compare_faces([stored_encoding], live_encoding)[0]
        return False
    
    def cast_vote(self, voter_id, candidate_id, proof_path):
        if self.votes.find_one({"voter_id": voter_id}):
            return False  # Already voted
        
        vote = {
            "voter_id": voter_id,
            "candidate_id": candidate_id,
            "timestamp": datetime.now(),
            "proof_image": proof_path
        }
        
        result = self.votes.insert_one(vote)
        if result.acknowledged:
            self.voters.update_one(
                {"_id": voter_id},
                {"$set": {"has_voted": True}}
            )
            return True
        return False
    
    def get_stats(self):
        total_voters = self.voters.count_documents({})
        total_votes = self.votes.count_documents({})
        
        pipeline = [
            {"$group": {"_id": "$candidate_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        vote_counts = list(self.votes.aggregate(pipeline))
        
        candidates = list(self.candidates.find({}))
        stats = {
            "total_voters": total_voters,
            "total_votes": total_votes,
            "vote_counts": vote_counts,
            "candidates": candidates
        }
        return stats
    
    def get_candidates(self):
        return list(self.candidates.find({}))
    
    def get_voters(self):
        return list(self.voters.find({}))