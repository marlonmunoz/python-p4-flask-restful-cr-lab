#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        try:
            plants = Plant.query.all()
            return [plant.to_dict() for plant in plants], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self):
        try:
            data = request.get_json()
            new_plant = Plant(name=data['name'], image=data['image'], price=data['price']) #  Create a new plant
            db.session.add(new_plant) #  Add the new plant to the session
            db.session.commit() #  Commit the session
            return new_plant.to_dict(), 201 #  Return the new plant as JSON with a 201 status code
        except Exception as e:
            return {'error': str(e)}, 500
        
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        try:
            plant = Plant.query.filter(Plant.id == id).first()
            if plant:
                return plant.to_dict(), 200
            else:
                return {'error': 'Plant not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    def post(self, id):
        try:
            plant = Plant.query.filter(Plant.id == id).first()
            if plant:
                data = request.get_json()
                plant.name = data['name']
                plant.image = data['image']
                plant.price = data['price']
                db.session.commit()
                return plant.to_dict(), 200
            else:
                return {'error': 'Plant not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    def delete(self, id):
        try:
            plant = Plant.query.filter(Plant.id == id).first()
            if plant:
                db.session.delete(plant)
                db.session.commit()
                return {}, 204
            else:
                return {'error': 'Plant not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
api.add_resource(PlantByID, '/plants/<int:id>') #  Add the new resource to the API
if __name__ == '__main__':
    app.run(port=5556, debug=True)
