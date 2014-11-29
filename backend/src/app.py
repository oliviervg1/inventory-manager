import os
import sqlalchemy
from collections import defaultdict
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from db import Session, bind_session_engine, tables
from models import Room, Item

app = Flask(__name__)
# The following allows @app.errorhandler(HTTPException) to work
app.config["TRAP_HTTP_EXCEPTIONS"] = True


@app.teardown_request
def shutdown_session(exception=None):
    Session.remove()


@app.errorhandler(HTTPException)
def http_error(error):
    response = jsonify(error=error.description)
    response.status_code = error.code
    return response


@app.errorhandler(sqlalchemy.orm.exc.NoResultFound)
def not_found(error):
    response = jsonify(error="Not found")
    response.status_code = 404
    return response


@app.errorhandler(sqlalchemy.exc.IntegrityError)
def already_exists(error):
    response = jsonify(error="Already exists")
    response.status_code = 409
    return response


@app.errorhandler(KeyError)
def key_error(error):
    response = jsonify(error="Invalid JSON")
    response.status_code = 400
    return response


@app.route("/rooms")
def get_rooms_and_their_content():
    session = Session()
    items = session.query(Item).all()
    data = defaultdict(list)
    for i in items:
        data[i.room.name].append(i.to_json())
    return jsonify(data)


@app.route("/rooms", methods=["POST"])
def add_room():
    session = Session()
    incoming_data = request.get_json()
    room = Room(incoming_data["name"])
    session.add(room)
    session.commit()
    response = jsonify(ref="/rooms/{0}".format(room.name))
    response.status_code = 201
    return response


@app.route("/rooms", methods=["DELETE"])
def remove_room():
    session = Session()
    incoming_data = request.get_json()
    room = session.query(Room).filter_by(name=incoming_data["name"]).one()
    session.query(Item).filter_by(room=room).delete()
    session.delete(room)
    session.commit()
    response = jsonify()
    response.status_code = 201
    return response


@app.route("/rooms/<room_name>/items/<item_name>")
def get_item(room_name, item_name):
    session = Session()
    room = session.query(Room).filter_by(name=room_name).one()
    item = session.query(Item).filter_by(room=room, name=item_name).one()
    return jsonify(item.to_json())


@app.route("/rooms/<room_name>/items/<item_name>", methods=["PUT"])
def add_item(room_name, item_name):
    session = Session()
    incoming_data = request.get_json()
    room = session.query(Room).filter_by(name=room_name).one()
    item = session.query(Item).filter_by(room=room, name=item_name).first()
    if not item:
        item = Item(
            item_name,
            room,
            incoming_data["weight"],
            incoming_data["description"],
            incoming_data["is_fragile"]
        )
        session.add(item)
    else:
        item.weight = incoming_data["weight"]
        item.description = incoming_data["description"]
        item.is_fragile = incoming_data["is_fragile"]
    session.commit()
    response = jsonify(ref="/rooms/{0}/items/{1}".format(room_name, item_name))
    response.status_code = 201
    return response


@app.route("/rooms/<room_name>/items/<item_name>", methods=["DELETE"])
def remove_item(room_name, item_name):
    session = Session()
    room = session.query(Room).filter_by(name=room_name).one()
    item = session.query(Item).filter_by(room=room, name=item_name).one()
    session.delete(item)
    session.commit()
    response = jsonify()
    response.status_code = 201
    return response


if __name__ == "__main__":

    if not os.path.exists("STATE_DIR"):
        os.mkdir("STATE_DIR")

    engine = bind_session_engine(
        "sqlite:///STATE_DIR/repos.db", encoding="utf-8"
    )

    if not os.path.exists("STATE_DIR/repos.db"):
        tables.metadata.create_all(engine)

        # Add fixture data
        session = Session()

        living_room = Room("living-room")
        tv = Item("TV", living_room, 80, "plasma screen", True)
        couch = Item("couch", living_room, 200, "leather", False)

        kitchen = Room("kitchen")
        fridge = Item("fridge", kitchen, 100, "Samsung fridge", True)

        session.add_all([living_room, couch, kitchen])
        session.add_all([tv, kitchen, fridge])
        session.commit()

    app.run(host="0.0.0.0", port=5000)
