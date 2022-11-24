from App.models import Command, VoteCommand
from App.database import db

def create_command():
    command = Command()
    # db.session.add(command)
    # db.session.commit()
    return command

def create_vote_command(review, staff, vote_type):
    command = VoteCommand(review, staff, vote_type)
    db.session.add(command)
    db.session.commit()
    return command

def get_all_vote_commands():
    commands = VoteCommand.query.all()
    return commands

def get_all_vote_commands_json():
    commands = VoteCommand.query.all()
    commands = [command.toJSON() for command in commands]
    return commands