import unittest
from mock import sentinel

from db import bind_session_engine, tables, Session
from models import Room, Item


class RoomTestCase(unittest.TestCase):

    def test_properties(self):
        room = Room(sentinel.name)
        self.assertEquals(room.name, sentinel.name)


class ItemTestCase(unittest.TestCase):

    def test_properties(self):
        item = Item(
            sentinel.room, sentinel.weight,
            sentinel.description, sentinel.is_fragile
        )
        self.assertEquals(item.room, sentinel.room)
        self.assertEquals(item.weight, sentinel.weight)
        self.assertEquals(item.description, sentinel.description)
        self.assertEquals(item.is_fragile, sentinel.is_fragile)


class TableMappingsTestCase(unittest.TestCase):

    def setUp(self):
        engine = bind_session_engine("sqlite:///:memory:", echo=False)
        tables.metadata.create_all(engine)
        self.session = Session()

        self.room = Room("living-room")
        self.item = Item(self.room, "80", "TV", True)
        self.session.add_all([self.room, self.item])
        self.session.commit()

    def test_room_relations(self):
        r = self.session.query(Room).one()
        self.assertTrue(isinstance(r, Room))
        self.assertTrue(r.name, "living-room")

    def test_item_relations(self):
        i = self.session.query(Item).one()
        self.assertTrue(isinstance(i, Item))
        self.assertTrue(i.room, self.room)
        self.assertTrue(i.weight, "80")
        self.assertTrue(i.description, "TV")
        self.assertTrue(i.is_fragile, True)
