from sqlalchemy import Column, Integer, String, Text, BLOB, ForeignKey, create_engine, select
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from flaskext.jsontools import JsonSerializableBase
from flask import json,jsonify
from app import app

engine = create_engine("mysql+pymysql://mysqluser:user@123@localhost:3306/ats")
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

    def __init__(self,name,skills,experience,email,address,mobileno,source,reffered_by,resume,status,current_ctc,expected_ctc,current_organization,notice_period):

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

@app.route("/add", methods = ["POST"])
def Insert():
    e=session.query(Employee).first()

    c1= Candidate("ABC","java,c,cpp",3,"abc@gmail.com","Pune","9087650987","referral",e.id,bytes(json.dumps("/home/user1/PycharmProjects/ats/a.txt"), 'utf8'),"Shortlisted",4,6,"niyuj",15)
    c2= Candidate("Shyamlee","c,cpp",5,"shyamlee@gmail.com","Pune","8907654908","referral",e.id,bytes(json.dumps("/home/user1/PycharmProjects/ats/a.txt"), 'utf8'),"Selected",7,10,"niyuj",10)

    session.add(c1)
    session.add(c2)
    session.commit()


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
