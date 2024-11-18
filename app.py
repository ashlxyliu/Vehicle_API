from flask import Flask
from database import db
import os
from schemas import Vehicle
from routes import init_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'

db.init_app(app)

os.makedirs('instance', exist_ok=True)

tables_created = False

init_routes(app)

@app.before_request
def create_tables_once():
    global tables_created
    if not tables_created:
        with app.app_context():
            db.create_all() 
            tables_created = True 

@app.route('/')
def home():
  return "Vehicle API"

if __name__ == '__main__':
  app.run(debug = True) 