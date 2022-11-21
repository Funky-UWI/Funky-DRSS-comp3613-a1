from App.database import db
from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import AbstractConcreteBase
from datetime import datetime


class Command(db.Model, AbstractConcreteBase):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.date = datetime.today()

    def execute(self):
        pass

    def undo(self):
        pass

    def toJSON(self):
        return {
            'id': self.id,
            'date': datetime.strftime(self.date, "%d/%m/%Y %H%:%M:%S")
        }
