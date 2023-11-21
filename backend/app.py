from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"@{os.environ.get('POSTGRES_HOST')}/{os.environ.get('POSTGRES_DB')}"
)
db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
