from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)



class Scientists(Resource):
    def get(self):
        scientists = [scientist.to_dict() for scientist in Scientist.query.all()]
        return scientists, 200


    def post(self):
        try:
            new_scientist = Scientist(
                name = request.form['name'],
                field_of_study = request.form['field_of_study'],
                avatar =  request.form['avatar'],
            )
            db.session.add(new_scientist)
            db.session.commit()
            return new_scientist.to_dict(), 201

        except:
            return {'error': 'Unable to create scientist'}, 400


class ScientistById(Resource):
    def get(self, id):
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            return scientist.to_dict(), 200
        except:
            return {'error': 'Scientist not found'}, 404


    def patch(self, id):
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            if scientist == None:
                return {'error': 'Scientist not found'}, 404
            else:
                for attr in request.form:
                    setattr(scientist, attr, request.form[attr])
                db.session.add(scientist)
                db.session.commit()
                return scientist.to_dict(), 200
        except:
            return {'error': 'Unable to update scientist'}, 400



    def delete(self, id):
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            db.session.delete(scientist)
            db.session.commit()
            return '', 204
        except:
            return {'error': 'Scientist not found'}, 404


class Planets(Resource):
    def get(self):
        planets = [planet.to_dict() for planet in Planet.query.all()]
        return planets, 200


class Missions(Resource):
    def post(self):
        try:
            new_mission = Mission(
                name = request.form['name'],
                scientist_id = request.form['scientist_id'],
                planet_id = request.form['planet_id'],
            )
            db.session.add(new_mission)
            db.session.commit()
            return new_mission.to_dict(), 401
        except:
            return {'error': 'Unable to create mission'}, 400




api.add_resource(Scientists, '/scientists')
api.add_resource(ScientistById, '/scientists/<int:id>')
api.add_resource(Planets, '/planets')
api.add_resource(Missions, '/missions')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
