from flask import Flask
from sqlalchemy import create_engine,update,and_
from models import Employee,Candidate,JobHasCandidate,JobPosition
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
    try:
        body = request.get_json()
        print(body)
        c =Candidate()
        c.deserialize(body)
        session.add(c)
        session.commit()
        return jsonify(c.serialize())
    except Exception as e:
        print(e)
    finally:
        session.rollback()


#Get Candidate Information
@app.route('/candidates/<id>', methods=['GET'])
def get_candidate(id):
    try:
        id=session.query(Candidate).get(id)
        return jsonify(id.serialize())
    except Exception as e:
        print(e)
    finally:
        session.rollback()
       # return "False"

#Update Candidate
@app.route('/candidates/<id>', methods = ['PUT'])
def update_candidate(id):
    try:
        print("id =" + id)
        db_value = session.query(Candidate).get(id)
        k = request.json
        #body = request.get_json()
        print(db_value.serialize())
        # c = Candidate()
        db_value.deserialize(k)
        session.commit()
        return jsonify(db_value.serialize())
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"


#Delete Candidate
@app.route('/candidates/<id>', methods = ['DELETE'])
def delete_candidate(id):
    try:
        d = session.query(Candidate).get(id)
        session.delete(d)
        session.commit()
        return {"Status":"Deleted Successfully"}
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"


#Get all Candidate
@app.route('/candidates/all', methods=["GET"])
def candidate_all():
    try:
        tmp_list = []
        stmt = session.query(Candidate).all()
        for result in stmt:
             tmp_list.append(result.serialize())
        return jsonify(tmp_list)
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"


#Get candidate By Source
@app.route('/candidates/source/<sourceid>', methods=['GET'])
def get_candidate_by_source(sourceid):
    try:
        print(sourceid)
        source=session.query(Candidate).filter(Candidate.source==sourceid)
        candidate_list = []
        for value in source:
            candidate_list.append(value.serialize())
        return jsonify(candidate_list)
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return ""


#Get candidate by Status
@app.route('/candidates/status/<status>', methods=['GET'])
def get_candidate_by_status(status):
    try:
        status=session.query(Candidate).filter(Candidate.status==status)
        candidate_list = []
        for value in status:
            candidate_list.append(value.serialize())
        return jsonify(candidate_list)
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"


#Get Shortlisted candidates for Job
@app.route('/candidates/job/<job_id>')
def get_candidate_by_job_id(job_id):
    try:
        candidate_list = []
        return_job = session.query(JobHasCandidate).filter(JobHasCandidate.position_id == job_id)
        for row in return_job:
          candidateid = row.candidate_id
          print(candidateid)
          # get list of candidate for that jobid
          result = session.query(Candidate).filter(and_(Candidate.id == candidateid , Candidate.status=="Shortlisted")).all()
          # Loop through  candidate list, convert to json and add to result list
          for candidate in result:
              candidate_list.append(candidate.serialize())
        return jsonify(candidate_list)
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"



#Create Job_Has_Candidate
@app.route("/job_has_candidate", methods = ["POST"])
def post_job_has_candidate():
    try:
        j_has_c = request.get_json()
        #print(j_has_c)
        c =JobHasCandidate()
        c.deserialize(j_has_c)
        session.add(c)
        session.commit()
        return jsonify(c.serialize())
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "false"

#Upload Resume
@app.route('/candidates/resume/<id>', methods = ['POST'])
def resume_upload(id):
    try:
        candidate = session.query(Candidate).get(id)
        f = request.files['resume']
        f.save('resume/' + f.filename)
        candidate.resume = 'resume/' + f.filename
        session.commit()
        return {"id": id,"status": "Resume Uploaded"}
    except Exception as e:
        print(e)
    finally:
        session.rollback()
        #return "False"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6000,debug=True)


