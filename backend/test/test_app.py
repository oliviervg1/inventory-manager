import unittest
import json

from db import Session, tables, bind_session_engine
from models import Room, Item
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        engine = bind_session_engine("sqlite:///:memory:")
        metadata = tables.metadata
        metadata.create_all(bind=engine)
        self.session = Session()

        # Fixture data
        self.room = Room("living-room")
        self.item = Item("TV", self.room, "80", "plasma screen", True)
        self.session.add_all([self.room, self.item])
        self.session.commit()

    def tearDown(self):
        Session.remove()

    def test_routing_error(self):
        r = self.app.get("/this/api/does/not/exist/yet")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            json.loads(r.data),
            {
                "error": ("The requested URL was not found on the server. "
                          " If you entered the URL manually please check your "
                          "spelling and try again.")
            }
        )

    def test_invalid_json_fails(self):
        r = self.app.post(
            "/rooms",
            content_type="application/json",
            data="THIS IS NOT JSON"
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            json.loads(r.data),
            {
                "error": "The browser (or proxy) sent a request that this "
                         "server could not understand."
            }
        )

    def test_add_room_already_exists(self):
        r = self.app.post(
            "/rooms",
            content_type="application/json",
            data=json.dumps({"name": "living-room"})
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(json.loads(r.data), {"error": "Already exists"})

    def test_add_room_success(self):
        r = self.app.post(
            "/rooms",
            content_type="application/json",
            data=json.dumps({"name": "kitchen"})
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"ref": "/rooms/kitchen"})

        # Check room has been added
        Session.remove()
        new_session = Session()
        self.assertEqual(len(new_session.query(Room).all()), 2)

    def test_remove_room_doesnt_exist(self):
        r = self.app.delete(
            "/rooms",
            content_type="application/json",
            data=json.dumps({"name": "doesnt-exist"})
        )
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), {"error": "Not found"})

    def test_remove_room_success(self):
        r = self.app.delete(
            "/rooms",
            content_type="application/json",
            data=json.dumps({"name": "living-room"})
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {})

        # Check room and related items have been deleted
        Session.remove()
        new_session = Session()
        self.assertEqual(len(new_session.query(Room).all()), 0)
        self.assertEqual(len(new_session.query(Item).all()), 0)

    def test_get_item(self):
        r = self.app.get("/rooms/living-room/items/TV")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            json.loads(r.data),
            {
                "description": "plasma screen",
                "is_fragile": True,
                "name": "TV",
                "weight": 80
            }
        )

    def test_add_item_room_doesnt_exist(self):
        r = self.app.put(
            "/rooms/non-existant/items/fridge",
            content_type="application/json",
            data=json.dumps({"name": "doesnt-exist"})
        )
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), {"error": "Not found"})

    def test_add_item_success(self):
        r = self.app.put(
            "/rooms/living-room/items/couch",
            content_type="application/json",
            data=json.dumps(
                {
                    "weight": 65,
                    "description": "Something to sit on",
                    "is_fragile": False
                }
            )
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            json.loads(r.data), {"ref": "/rooms/living-room/items/couch"}
        )

        # Check item has been added
        Session.remove()
        new_session = Session()
        item = new_session.query(Item).filter_by(name="couch").one()
        self.assertEqual(item.description, "Something to sit on")

    def test_update_item_success(self):
        r = self.app.put(
            "/rooms/living-room/items/TV",
            content_type="application/json",
            data=json.dumps(
                {
                    "weight": 120,
                    "description": "Cathode tv",
                    "is_fragile": False
                }
            )
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            json.loads(r.data), {"ref": "/rooms/living-room/items/TV"}
        )

        # Check item has been updated
        Session.remove()
        new_session = Session()
        items = new_session.query(Item).all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Cathode tv")

    def test_remove_item_doesnt_exist(self):
        r = self.app.delete("/rooms/living-room/items/non-existant")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), {"error": "Not found"})

    def test_remove_item_success(self):
        r = self.app.delete("/rooms/living-room/items/TV")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {})

        # Check room is still there but item has been deleted
        Session.remove()
        new_session = Session()
        self.assertEqual(len(new_session.query(Room).all()), 1)
        self.assertEqual(len(new_session.query(Item).all()), 0)

    def test_get_items(self):
        r = self.app.get("/rooms")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            json.loads(r.data),
            {
                "living-room": [{
                    "name": "TV",
                    "description": "plasma screen",
                    "weight": 80,
                    "is_fragile": True
                }]
            }
        )
