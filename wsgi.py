import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import create_user, get_all_users_json, get_all_users
from App.controllers import *

from datetime import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f"{username} created!")


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli

"""
COMMAND commands
"""

command_cli = AppGroup("command", help="Command object commands")


# Then define the command and any parameters and annotate it with the group (@)
@command_cli.command("create", help="Creates a command")
def create_generic_command():
    command = create_command()
    print(f"{command.toJSON()} created!")


@command_cli.command("upvote", help="Creates a command")
@click.argument('staff_id', default=1)
def create_upvote_command(staff_id):
    staff = get_user(staff_id)
    command = create_vote_command(None, staff, "upvote")
    print(f"{command.toJSON()} created!")

@command_cli.command("downvote", help="Creates a command")
def create_upvote_command():
    command = create_vote_command(None, None, "downvote")
    print(f"{command.toJSON()} created!")

@command_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_vote_commands())
    else:
        print(get_all_vote_commands_json())


app.cli.add_command(command_cli)  # add the group to the cli


"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database intialized")


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


@test.command("review", help="Run Student tests")
@click.argument("type", default="all")
def review_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


@test.command("command", help="Run Command tests")
@click.argument("type", default="all")
def command_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "CommandUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "CommandIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("votecommand", help="Run VoteCommand tests")
@click.argument("type", default="all")
def votecommand_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "VoteCommandUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "VoteCommandIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)
