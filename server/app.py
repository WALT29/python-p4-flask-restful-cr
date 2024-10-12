#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict={
             "message": "Welcome to the Newsletter RESTful API",
        }
        return make_response(response_dict,200)
api.add_resource(Home,'/')


class Newsletters(Resource):
    def get(self):
        response_dict=[n.to_dict() for n in Newsletter.query.all()]
        return make_response(response_dict,200)
    
    def post(self):
        new_record=Newsletters(
            title=request.form.get("title"),
            body=request.form.get("body")
            
        )
        db.session.add(new_record)
        db.session.commit()
        
        new_record_dict=new_record.to_dict
        
        return make_response(new_record_dict,201)

api.add_resource(Newsletters,'/newsletters')

class Newsletter_by_id(Resource):
    def get(self,id):
        record=Newsletter.query.filter_by(id=id).first().to_dict()
        
        return make_response(record,200)
api.add_resource(Newsletter_by_id,'/newsletters/<int:id>')





if __name__ == '__main__':
    app.run(port=5555, debug=True)
