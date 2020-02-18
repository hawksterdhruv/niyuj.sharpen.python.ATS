from sqlalchemy import Column, Integer, String, Text, BLOB, ForeignKey, create_engine, select
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from flaskext.jsontools import JsonSerializableBase
from flask import json,jsonify, request
from app import app

engine = create_engine("mysql+pymysql://root:tos1byte@localhost:3306/ats")
connection=engine.connect()
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(100),
                  nullable=False)
    email = Column(String(100),
                   nullable=False)
    address = Column(String(100),
                     nullable=False)
    mobileno = Column(String(10),
                      nullable=False)

    # relationship
    candidate_ref = relationship("Candidate", backref="reference")

    def __init__(self, name, email, address, mobileno):
        self.name = name
        self.email = email
        self.address = address
        self.mobileno = mobileno


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(100),
                  nullable=False)
    email = Column(String(100),
                  nullable=False)
    address = Column(String(100),
                  nullable=False)
    mobileno = Column(String(10),
                  nullable=False)
    skills = Column(Text,
                  nullable=True)
    experience = Column(Integer,
                  nullable=False)
    source = Column(String(100))
    reffered_by = Column(Integer,
                   ForeignKey('employee.id'),
                   nullable=False)
    resume = Column(BLOB,
                  nullable=False)
    status = Column(String(100),
                  nullable=False)
    current_ctc = Column(Integer,
                         nullable=False)
    expected_ctc = Column(Integer,
                         nullable=False)
    current_organization = Column(String(100))

    notice_period = Column(Integer)

    def __init__(self,name=None, skills=None,experience=None,email=None,address=None,mobileno=None,source=None,reffered_by=None,resume=None,status=None,current_ctc=None,expected_ctc=None,current_organization=None,notice_period=None):

        self.name=name
        self.email=email
        self.address=address
        self.mobileno=mobileno
        self.skills=skills
        self.experience=experience
        self.source=source
        self.reffered_by=reffered_by
        self.resume=resume
        self.status=status
        self.current_ctc=current_ctc
        self.expected_ctc=expected_ctc
        self.current_organization=current_organization
        self.notice_period=notice_period

    def serialize(self):
        return {
         'id' : self.id,
         'name': self.name,
         'email': self.email,
         'address': self.address,
         'mobileno': self.mobileno,
         'skills': self.skills,
         'experience' : self.experience,
         'source' : self.source,
         'reffered_by' : self.reffered_by,
         #'resume' : self.resume,
         'status' : self.status,
         'current_ctc' : self.current_ctc,
         'expected_ctc' : self.expected_ctc,
         'current_organization' : self.current_organization,
         'notice_period' : self.notice_period
        }

    def deserialize(self, candidate_json):
        self.id = candidate_json.get('id')
        self.name = candidate_json.get('name')
        self.email = candidate_json.get('email')
        self.address = candidate_json.get('address')
        self.mobileno = candidate_json.get('mobileno')
        self.skills = candidate_json.get('skills')
        self.experience = candidate_json.get('experience')
        self.source = candidate_json.get('source')
        self.reffered_by = candidate_json.get('reffered_by')
        self.resume = candidate_json.get('resume').encode()
        self.status = candidate_json.get('status')
        self.current_ctc = candidate_json.get('current_ctc')
        self.expected_ctc = candidate_json.get('expected_ctc')
        self.current_organization = candidate_json.get('current_organization')
        self.notice_period = candidate_json.get('notice_period')

@app.route("/add", methods = ["POST"])
def Insert():
    body = request.get_json()
    print(body)
    c =Candidate()
    c.deserialize(body)
    session.add(c)
    session.commit()
    return jsonify(c.serialize())


@app.route('/all', methods=["GET"])
def Show():
        tmp_list = []
        try:
            stmt = session.query(Candidate).all()
            for result in stmt:
                tmp_list.append(result.serialize())
        except Exception as e:
            print(e)
        return jsonify(tmp_list)

if __name__ == "__main__":
    app.run(debug=True)
