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
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    # review = db.relationship("Review", back_populates="votecommand")
    review = db.relationship("Review", back_populates="votes")

    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    staff = db.relationship("User")
    # ensures user only votes once
    __table_args__ = (db.UniqueConstraint('staff_id', 'review_id', name='review_staff'),
                     )

    def __init__(self, review_id, staff_id, vote_type):
        # self.date = date
        super().__init__()
        self.vote_type = VoteTypeDict[vote_type]
        # self.review = review
        self.review_id = review_id
        # self.staff = staff
        self.staff_id = staff_id

    # def execute(self):
    #     self.review.vote(self.staff_id, self.vote_type)
    #     # return super().execute()

    # def undo(self):
    #     if self.vote_type==1:
    
    def toJSON(self):
        return {
            'id': self.id,
            'vote_type': self.vote_type,
            'date': super().toJSON()['date'],
            'review': self.review.toJSON(),
            'staff': self.staff.toJSON()
        }