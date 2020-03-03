from flask import Flask
from sqlalchemy import create_engine,update
from models import Employee,Candidate,JobHasCandidate
from sqlalchemy.orm import sessionmaker
from flask import json,jsonify,request
from db import session
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Application Tracking System"


#Create Candidate
@app.route("/candidates", methods = ["POST"])
def post_candidate():
    body = request.get_json()
    print(body)
    c =Candidate()
    c.deserialize(body)
    session.add(c)
    session.commit()
    return jsonify(c.serialize())

#Get Candidate Information
@app.route('/candidates/<id>', methods=['GET'])
def get_candidate(id):
    id=session.query(Candidate).get(id)
    return jsonify(id.serialize())

'''
#Update Candidate
@app.route('/candidates/<id>', methods = ['PUT'])
def update_candidate(id):
'''


#Delete Candidate
@app.route('/candidates/<id>', methods = ['DELETE'])
def delete_candidate(id):
    d = session.query(Candidate).get(id)
    session.delete(d)
    session.commit()
    return {"Status":"Deleted Successfully"}

#Get all Candidate
@app.route('/candidates/all', methods=["GET"])
def candidate_all():
        tmp_list = []
        stmt = session.query(Candidate).all()
        for result in stmt:
             tmp_list.append(result.serialize())
        return jsonify(tmp_list)

#Create Job_Has_Candidate
@app.route("/job_has_candidate", methods = ["POST"])
def post_job_has_candidate():
    body = request.get_json()
    print(body)
    c =JobHasCandidate()
    c.deserialize(body)
    session.add(c)
    session.commit()
    return jsonify(c.serialize())


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6000,debug=True)

