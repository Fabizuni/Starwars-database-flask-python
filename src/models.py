from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

               
class Planets(db.Model):
    plaid = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    diameter = db.Column(db.String(100))
    rotation_period = db.Column(db.String(100))
    orbital_period = db.Column(db.String(100))
    gravity = db.Column(db.String(100))
    population = db.Column(db.String(100))
    Climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    surface_water = db.Column(db.String(100))
    

    def __repr__(self):
        return '<Planets %r>' % self.full_name

    def serialize(self):
        return {
            "plaid": self.plaid,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "Climate": self.Climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
                             
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    chaid = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    height = db.Column(db.String(100))
    mass = db.Column(db.String(100))
    hair_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    gender = db.Column(db.String(100))
 

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "chaid": self.chaid,
            "full_name": self.full_name,
            "description": self.description,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "gender": self.gender,
            "birth_year": self.birth_year,
           
            # do not serialize the password, its a security breach
        }

   

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship("Favorites", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "userid": self.userid,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "favorites": list(map(lambda x: x.serialize(), self.favorites))
            # do not serialize the password, its a security breach
        }
        

class Favorites(db.Model):
    favid = db.Column(db.Integer, primary_key=True)
    user_userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    tipo = db.Column(db.String(100))
    object_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Favorites %r>' % self.favid

    def serialize(self):
        return {
            "favid": self.favid,
            "user_userid":self.user_userid,
            "tipo": self.tipo,
            "object_id": self.object_id,
                    
            # do not serialize the password, its a security breach
        }
