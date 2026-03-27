from database.mongodb_client import MongoDBClient

class VotingService:
    def __init__(self):
        self.db = MongoDBClient()
    
    def can_vote(self, voter_id):
        voter = self.db.voters.find_one({"_id": voter_id, "has_voted": False})
        return voter is not None