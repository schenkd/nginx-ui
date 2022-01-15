import os
from app.backend import create_app
from flask_cors import CORS


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
