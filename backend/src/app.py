import os
from flask import Flask

from db import bind_session_engine, tables

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    if not os.path.exists("STATE_DIR"):
        os.mkdir("STATE_DIR")
    engine = bind_session_engine("sqlite:///STATE_DIR/repos.db")

    if not os.path.exists("STATE_DIR/repos.db"):
        tables.metadata.create_all(engine)

    # The following allows @app.errorhandler(HTTPException) to work
    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    app.run(host="0.0.0.0", port=5000)
