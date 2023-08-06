from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class FavoritesChar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey("people.id")) #many to one
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #many to one

    def to_dict(self):
        return {
            'id': self.id,
            'char_id': self.char_id,
            'user_id': self.user_id,            
        }

class FavoritesPlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id")) #many to one
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #many to one
    def to_dict(self):
        return {
            'id': self.id,
            'planet_id': self.planet_id,
            'user_id': self.user_id,            
        }

class people(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250),nullable=False)
    birth_year =db.Column(db.Integer)
    gender = db.Column(db.String(25))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(25))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'gender': self.gender,
            'height': self.height,
            'skin_color': self.skin_color
        }


class Planet(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    climate = db.Column(db.String(25))
    gravity = db.Column(db.Integer)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(25))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'gravity': self.gravity,
            'population': self.population,
            'terrain': self.terrain
            
        }