from SetupDb import db_session
import SetupDb
#from interview_model import Interview
from models import Interview , JobHasCandidate , JobPosition
import datetime
from datetime import datetime, timedelta

from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

SetupDb.init_db()
# dummyInterviewdata = Interview(2,2,"F2F", "Niyuj HQ", "NA", "NA", datetime.datetime.now())
#
# db_session.add(dummyInterviewdata)
# db_session.commit()


@app.route('/interviews')
def get_interviews():
    interviews = db_session.query(Interview).all()
    interview_list = []
    for interview in interviews:
        interview_list.append(interview.serialize())
    return jsonify(interview_list)


@app.route('/interviews/candidate/<candi_id>')
def get_interviews_by_candidate_id(candi_id):
    interview_list = []
    # Get entries from JobHasCandidate table for the specific candidate id
    return_interview = db_session.query(JobHasCandidate).filter(JobHasCandidate.candidate_id == candi_id)
    for row in return_interview:
      jhcid = row.id
      # get list of interviews for that job_has_candidate_id
      result = db_session.query(Interview).filter(Interview.job_has_candidate_id == jhcid)
      # Loop through  interview list, convert to json and add to result list
      for interview in result:
          interview_list.append(interview.serialize())
    return jsonify(interview_list)


@app.route('/interviews/job/<job_id>')
def get_interviews_by_job_id(job_id):
    interview_list1 = []
    return_job = db_session.query(JobHasCandidate).filter(JobHasCandidate.position_id == job_id)
    for row in return_job:
      jhcid = row.id
      print(jhcid)
      # get list of interviews for that job_has_candidate_id
      result11 = db_session.query(Interview).filter(Interview.job_has_candidate_id == jhcid)
      # Loop through  interview list, convert to json and add to result list
      for interview in result11:
          interview_list1.append(interview.serialize())
    return jsonify(interview_list1)


@app.route('/interviews/<id>')
def get_interview(id):
    interview_obj = db_session.query(Interview).get(id)
    if interview_obj == None:
        abort(404)
    return jsonify(interview_obj.serialize())



@app.route('/interviews/<id>', methods = ['DELETE'])
def delete_interview(id):
    x = db_session.query(Interview).get(id)
    db_session.delete(x)
    db_session.commit()
    return {"status": "OK"}

@app.route('/interviews/schedule', methods = ['POST'])
def post_interview():
   content = request.get_json()
   interviewObj = Interview(content)
   db_session.add(interviewObj)
   db_session.commit()
   return {"id": interviewObj.id,"status": "OK"}

@app.route('/interviews/schedule/<id>', methods = ['PUT'])
def update_interview(id):
   content = request.get_json()
   interviewUpdatedObj = Interview(content)
   # interviewObj.id = id
   # db_session.add(interviewObj)
   interviewObj = db_session.query(Interview).get(id)
   interviewObj = interviewUpdatedObj
   db_session.commit()
   return {"id": interviewObj.id,"status": "OK"}


@app.route('/interviews/days/<days>')
def get_interview_by_date(days):
    current_date = datetime.now()
    search_date = datetime.now() + timedelta(days=int(days))
    results = db_session.query(Interview).filter(Interview.schedule_time.between(current_date, search_date))
    date_list = []
    for value in results:
        date_list.append(value.serialize())
    return jsonify(date_list)

@app.route('/interviews/<id>/feedback', methods = ['PATCH'])
def patch_interview(id):
    content = request.get_json()
    db_value = db_session.query(Interview).get(id)
    key_list = content.keys()
    if 'comment' in key_list:
        db_value.comment = content['comment']
    if 'feedback' in key_list:
        db_value.feedback = content['feedback']
    db_session.commit()
    return {"id": id,"status": "Feedback recorded"}

@app.route('/interviews/schedule/<id>', methods = ['PUT'])
def put_interview(id):
    content = request.get_json()
    delete_interview(id)
    interviewObj = Interview(content,id)
    db_session.add(interviewObj)
    db_session.commit()
    return {"id": interviewObj.id, "status": "Updated"}

if __name__ == '__main__':
   app.run(port=4000)
