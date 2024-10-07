from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    user_name = db.Column(db.String(250), unique=False, nullable=False)
    user_lastname = db.Column(db.String(250), unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, email, password, user_name, user_lastname, date):
        self.email = email
        self.password = password
        self.user_name = user_name
        self.user_lastname = user_lastname
        self.date = date
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'user_name': self.user_name,
            'user_lastname': self.user_lastname,
            'date': self.date,
            'is_active': self.is_active,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    personaje = db.Column(db.String(50), unique=True, nullable=False)
    planeta_origen = db.Column(db.String(50), unique=True, nullable=False)
    altura = db.Column(db.String(50), unique=True, nullable=False)
    peso = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, personaje, planeta_origen, altura, peso):
        self.personaje = personaje
        self.planeta_origen = planeta_origen
        self.altura = altura
        self.peso = peso

    def serialize(self):
        return {
            'personaje' : self.personaje,
            'planeta_origen' : self.planeta_origen,
            'altura' : self.altura,
            'peso' : self.peso,
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), unique=True, nullable=False)
    poblacion = db.Column(db.String(50), unique=False, nullable=False)
    clima = db.Column(db.String(50), unique=False, nullable=False)
    diametro = db.Column(db.Integer, nullable=False)
    periodo_rotacion = db.Column(db.Integer, nullable=False)
    
    def __init__(self, planet_name, poblacion, clima, diametro, periodo_rotiacion):
        self.planet_name = planet_name
        self.poblacion = poblacion
        self.clima = clima
        self.diametro = diametro
        self.periodo_rotacion = periodo_rotiacion
        
    def serialize(self):
        return {
            'planet_name' : self.planet_name,
            'poblacion' : self.poblacion,
            'clima' : self.clima,
            'diametro' : self.diametro,
            'periodo_rotacion' : self.periodo_rotacion
        }

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    planet = db.relationship("Planets")


    personaje_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=False)
    personaje = db.relationship("Characters")

    def __init__(self, user, planet, personaje):
        self.user = user
        self.planet = planet
        self.personaje = personaje

    def serialize (self):
        return {
            'user' : self.user.serialize(),
            'planet' : self.planet.serialize(),
            'personaje' : self.personaje.serialize(),
        }
