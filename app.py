from flask import *
from flask_socketio import *
import os
import random
from string import ascii_uppercase

from flask_socketio import SocketIO

from backend.models.models import *
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)
socketio: SocketIO = SocketIO(app, engineio_logger=True, async_handlers=True)

from backend.base_route.route import *
from backend.contact.route import *
from backend.user_basics.basic import *

if __name__ == '__main__':
    socketio.run(app, debug=True)
