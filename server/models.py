from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    serialize_rules = ('-scientist.missions', '-planet.missions',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')

    @validates('name')
    def validates_name(self, key, name):
        if name == '':
            raise ValueError("Must enter a name")
        return name

    @validates('scientist_id')
    def validates_name(self, key, scientist):
        if scientist == '' or scientist == 'NULL':
            raise ValueError("Must enter a scientist")
        return scientist

    @validates('planet_id')
    def validates_name(self, key, planet):
        if planet == '' or planet == 'NULL':
            raise ValueError("Must enter a planet")
        return planet


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-missions',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship('Mission', back_populates='scientist')
    planets = association_proxy('missions', 'planet')

    @validates('name')
    def validates_name(self, key, name):
        if name == '':
            raise ValueError("Must enter a name")
        return name

    @validates('field_of_study')
    def validates_field_of_study(self, key, field):
        if field == '':
            raise ValueError("Must enter a field of study")
        return field


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    serialize_rules = ('-scientists.planet',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship('Mission', back_populates='planet')
    scientists = association_proxy('missions', 'scientist')
