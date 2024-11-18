from database import db

class Vehicle(db.Model):
  vin_number = db.Column(db.String(17), primary_key = True)
  manufacturer_name = db.Column(db.String(50))
  description = db.Column(db.String(200))
  horse_power = db.Column(db.Integer)
  model_name = db.Column(db.String(50))
  model_year = db.Column(db.Integer)
  purchase_price = db.Column(db.Float)
  fuel_type = db.Column(db.String(20))

  def to_dictionary(self):
    return {
      "vin_number": self.vin_number,
      "manufacturer_name": self.manufacturer_name,
      "description": self.description,
      "horse_power": self.horse_power,
      "model_name": self.model_name, 
      "model_year": self.model_year,
      "purchase_price": self.purchase_price,
      "fuel_type": self.fuel_type
    }
