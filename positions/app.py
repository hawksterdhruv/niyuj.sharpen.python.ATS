from flask import Flask, request, jsonify, abort, make_response
import json
from models import Project, JobPosition, Employee
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy import create_engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


engine = create_engine("mysql+pymysql://root:tos1byte@localhost/ats")
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/projects')
def get_projects():
    resList = []
    result = session.query(Project).all()
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/employees')
def get_employees():
    resList = []
    result = session.query(Employee).all()
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/positions')
def get_positions():
    resList = []
    result = session.query(JobPosition).all()
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)


@app.route('/positions', methods=['POST'])
def create_position():
    try:
        jp = JobPosition()
        data = request.get_json()
        jp.deserialize(data)
        session.add(jp)
        session.commit()
        return jsonify(jp.serialize), 201
    except Exception as e:
        print(e)
        session.rollback()
        return jsonify({}), 500

@app.route('/positions/<id>', methods=['GET'])
def get_position_by_id(id):
    result = session.query(JobPosition).get(id)
    if result:
        return jsonify(result.serialize)
    else:
        return jsonify({})

@app.route('/positions/skill/<skills>', methods=['GET'])
def get_position_by_skill(skills):
    resList = []
    # result = session.query(JobPosition).filter_by(skills=skills)
    result = session.query(JobPosition).filter(JobPosition.skills.contains(skills))
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/positions/grade/<grade>', methods=['GET'])
def get_position_by_grade(grade):
    resList = []
    result = session.query(JobPosition).filter(JobPosition.grade.in_(grade))
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/positions/projectid/<projectid>', methods=['GET'])
def get_position_by_projectid(projectid):
    resList = []
    result = session.query(JobPosition).filter(JobPosition.project_id.__eq__(projectid))
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/positions/experience/<experience>', methods=['GET'])
def get_position_by_experience(experience):
    resList = []
    result = session.query(JobPosition).filter(JobPosition.experience.in_(experience))
    for row in result:
        resList.append(row.serialize)
    return jsonify(resList)

@app.route('/positions/update/<id>', methods=['PUT'])
def update_position_by_id(id):
    try:
        jobPosition = session.query(JobPosition).get(id)
        data = request.get_json()
        if 'skills' in data:
            jobPosition.skills = data['skills']
        if 'experience' in data:
            jobPosition.experience = data['experience']
        if 'no_of_openings' in data:
            jobPosition.no_of_openings = data['no_of_openings']
        if 'title' in data:
            jobPosition.title = data['title']
        if 'status' in data:
            jobPosition.status = data['status']
        if 'grade' in data:
            jobPosition.grade = data['grade']
        if 'project_id' in data:
            jobPosition.project_id = data['project_id']
        if 'employee_id' in data:
            jobPosition.employee_id = data['employee_id']

        session.commit()
        return jsonify(jobPosition.serialize)
    except Exception as e:
        print(e)
        session.rollback()
        return jsonify({}), 500

@app.route('/positions/<id>', methods=['DELETE'])
def delete_position_by_id(id):
    try:
        jobPosition = session.query(JobPosition).get(id)
        session.delete(jobPosition)
        session.commit()
        return jsonify({'response': 'Success'})
    except Exception as e:
        print(e)
        session.rollback()
        return jsonify({'response': 'Id not found'}), 500

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True,port=7000,host='0.0.0.0')
