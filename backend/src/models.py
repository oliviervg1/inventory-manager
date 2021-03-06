from db import tables
from sqlalchemy.orm import mapper, relation


class Room(object):

    def __init__(self, name):
        self.name = name


class Item(object):

    def __init__(self, name, room, weight, description, is_fragile):
        self.name = name
        self.room = room
        self.weight = weight
        self.description = description
        self.is_fragile = is_fragile

    def to_json(self):
        return {
            "name": self.name,
            "weight": self.weight,
            "description": self.description,
            "is_fragile": self.is_fragile
        }


mapper(Room, tables.rooms)
mapper(Item, tables.items, properties={
    "room": relation(Room),
})
