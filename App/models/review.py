from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.relationship('VoteCommand', back_populates="review", cascade="all, delete")


    def __init__(self, user_id, student_id, text):
        self.user_id = user_id
        self.student_id = student_id
        self.text = text


    def get_num_upvotes(self):
        num_upvotes=0
        for votecommand in self.votes:
            if votecommand.vote_type==1:
                num_upvotes+=1
        return num_upvotes

    def get_num_downvotes(self):
        num_downvotes=0
        for votecommand in self.votes:
            if votecommand.vote_type==-1:
                num_downvotes+=1
        return num_downvotes

    def get_karma(self):
        return self.get_num_upvotes() - self.get_num_downvotes()

    def get_all_votes(self):
        num_votes=0
        for votecommand in self.votes:
            num_votes+= 1
        return num_votes

    def toJSON(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "text": self.text,
            "karma": self.get_karma(),
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
