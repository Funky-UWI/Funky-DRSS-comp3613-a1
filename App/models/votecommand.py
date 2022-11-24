from App.database import db
from .command import Command
import enum
from sqlalchemy import Enum, Table

class VoteTypeEnum(enum.Enum):
    upvote = 1
    downvote = -1

VoteTypeDict = {
    "upvote": 1,
    "downvote": -1,
}

class VoteCommand(Command):
    
    # vote_type = db.Column(db.Enum(VoteTypeEnum), nullable=False)
    vote_type = db.Column(db.Integer, nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=True)
    # review = db.relationship("Review", back_populates="votecommand")
    review = db.relationship("Review")

    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    staff = db.relationship("User")

    def __init__(self, review, staff, vote_type):
        # self.date = date
        super().__init__()
        self.vote_type = VoteTypeDict[vote_type]
        self.review = review
        self.staff = staff

    def execute(self):
        # review.upvote
        return super().execute()

    def undo(self):
        pass
    
    def toJSON(self):
        return {
            'id': self.id,
            'vote_type': self.vote_type,
            'date': super().toJSON()['date'],
            'review': self.review.toJSON(),
            'staff': self.staff.toJSON()
        }