from App.models import Command, VoteCommand
from App.controllers.review import *
from App.controllers.user import *
from App.database import db
from sqlalchemy import and_

def create_command():
    command = Command()
    # db.session.add(command)
    # db.session.commit()
    return command

def create_vote_command(review_id, staff_id, vote_type):
    command = VoteCommand(review_id, staff_id, vote_type)
    db.session.add(command)
    db.session.commit()
    return command

# def create_vote_command(review_id, staff_id, vote_type):
#     review = get_review(review_id)
#     staff = get_user(staff_id)
#     command = VoteCommand(review, staff, vote_type)
#     db.session.add(command)
#     db.session.commit()
#     return command

def get_all_vote_commands():
    commands = VoteCommand.query.all()
    return commands

def get_all_vote_commands_json():
    commands = VoteCommand.query.all()
    commands = [command.toJSON() for command in commands]
    return commands

def get_votes_by_staff(staff_id):
    votes = VoteCommand.query.filter_by(staff_id = staff_id)
    return votes

def get_upvotes_by_review(review_id):
    votes = VoteCommand.query.filter_by(review_id = review_id, vote_type = 1)
    return [vote.toJSON() for vote in votes]

def get_downvotes_by_review(review_id):
    votes = VoteCommand.query.filter_by(review_id = review_id, vote_type = -1)
    return votes

def get_votes_by_review(review_id):
    votes = VoteCommand.query.filter_by(review_id = review_id)
    return votes

def get_vote(id):
    vote = VoteCommand.query.get(id)
    return vote