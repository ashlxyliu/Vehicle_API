from flask import Flask
from database import db
# import os
from schemas import Vehicle

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/vehicles.db'

db.init_app(app)

@app.before_request
def create_tables_once():
  with app.app_context():
    db.create_all()

@app.route('/')
def home():
  return "Vehicle API"

if __name__ == '__main__':
  # os.makedirs('instance', exist_ok=True)
  app.run(debug = True) 