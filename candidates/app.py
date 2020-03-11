from flask import Flask,abort
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
    # finally:
        session.rollback()
        return jsonify({'Response': 'Not created'}), 500


#Get Candidate Information
@app.route('/candidates/<id>', methods=['GET'])
def get_candidate(id):
    try:
        candidate_record = session.query(Candidate).get(id)
        if candidate_record:
            return jsonify(candidate_record.serialize())
        else:
            return jsonify({})

    except Exception as e:
        print(e)
    # finally:
        session.rollback()
        return jsonify({'Response': 'Id not found'}), 500



#Update Candidate
@app.route('/candidates/<id>', methods = ['PUT'])
def update_candidate(id):
    try:
        print("id =" + id)
        candidate_record = session.query(Candidate).get(id)
        if candidate_record:
            k = request.json
            #body = request.get_json()
            print(candidate_record.serialize())
            # c = Candidate()
            candidate_record.deserialize(k)
            session.commit()
            return jsonify(candidate_record.serialize())
        else:
            return jsonify({})

    except Exception as e:
        print(e)
    # finally:
        session.rollback()
        return jsonify({'Response': 'Id not found'}), 500


#Delete Candidate
@app.route('/candidates/<id>', methods = ['DELETE'])
def delete_candidate(id):
    try:
        candidate_record = session.query(Candidate).get(id)
        if candidate_record:
            session.delete(candidate_record)
            session.commit()
            return {"response":"Deleted Successfully"}
        else:
            return jsonify({})

    except Exception as e:
        print(e)
    # finally:
        session.rollback()
        return jsonify({'Response': 'Id not found'}), 500

#Get all Candidate
@app.route('/candidates/', methods=["GET"])
def candidate_all():
    # try:
    tmp_list = []
    candidate_record = session.query(Candidate).all()
    if candidate_record:
        for result in candidate_record:
             tmp_list.append(result.serialize())
        return jsonify(tmp_list)
    else:
        return jsonify({})
    # except Exception as e:
    #     print(e)
    # finally:
    #     session.rollback()
    #     return "False"


#Get candidate By Source
@app.route('/candidates/source/<sourcename>', methods=['GET'])
def get_candidate_by_source(sourcename):
    # try:
        #print(sourcename)
    source=session.query(Candidate).filter(Candidate.source==sourcename)
    if source:
        candidate_list = []
        for value in source:
            candidate_list.append(value.serialize())
        return jsonify(candidate_list)
    else:
        return jsonify({})


#Get candidate by Status
@app.route('/candidates/status/<status>', methods=['GET'])
def get_candidate_by_status(status):
    # try:
    status=session.query(Candidate).filter(Candidate.status==status)
    if status:
        candidate_list = []
        for value in status:
            candidate_list.append(value.serialize())
        return jsonify(candidate_list)
    else:
        return jsonify({})
    # except Exception as e:
    #     print(e)
    # finally:
    #     session.rollback()
        #return "False"


#Get Shortlisted candidates for Job
@app.route('/candidates/<id>/positions', methods=['GET'])
def get_job_by_candidate_id(id):
    # try:
    job_list = []
    return_job = session.query(JobHasCandidate).filter(JobHasCandidate.candidate_id == id)
    if return_job:
        for row in return_job:
            # print(row.jobposition.serialize)
            positionid = row.position_id
            print(positionid)
            # result = session.query(JobPosition).filter(JobPosition.id == positionid).all()
            # for job in result:
            job_list.append(row.jobposition.serialize)
        return jsonify(job_list)
    else:
        return jsonify({})
    # except Exception as e:
    #     print(e)
    # finally:
    #     session.rollback()
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
    # finally:
        session.rollback()
        return jsonify({})

#Upload Resume
@app.route('/candidates/resume/<id>', methods = ['POST'])
def resume_upload(id):
    try:
        candidate = session.query(Candidate).get(id)
        f = request.files['resume']
        f.save('resume/' + f.filename)
        candidate.resume = 'resume/' + f.filename
        session.commit()
        return {"id": id,"Response": "Resume Uploaded"}
    except Exception as e:
        print(e)
    # finally:
        session.rollback()
        return jsonify({'response': 'Id not found'}), 500

        # return jsonify({})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)


