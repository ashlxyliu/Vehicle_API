from flask import Flask
from database import db
from schemas import Vehicle
from routes import init_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'

db.init_app(app)

init_routes(app)

@app.before_request
def create_tables_once():
  with app.app_context():
    db.create_all()

@app.route('/')
def home():
  return "Vehicle API"

if __name__ == '__main__':
  app.run(debug = True) 