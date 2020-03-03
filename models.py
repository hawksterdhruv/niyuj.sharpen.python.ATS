from datetime import datetime
from pprint import pprint

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import json

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# from model import *
Base = declarative_base()

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
    job_positions = relationship('JobPosition', back_populates="employee")

    def __init__(self, name, email, address, mobileno):
        self.name = name
        self.email = email
        self.address = address
        self.mobileno = mobileno

    @property
    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "mobileno": self.mobileno,
        }



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
    resume = Column(String(50),
                  nullable=False)
    status = Column(String(100),
                  nullable=False)
    current_ctc = Column(Integer)
    expected_ctc = Column(Integer)
    current_organization = Column(String(100))

    notice_period = Column(Integer)

    #Relationship
    #reference = relationship("Employee",back_populates="candidate")

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
         'resume' : self.resume,
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
        self.resume = candidate_json.get('resume')
        self.status = candidate_json.get('status')
        self.current_ctc = candidate_json.get('current_ctc')
        self.expected_ctc = candidate_json.get('expected_ctc')
        self.current_organization = candidate_json.get('current_organization')
        self.notice_period = candidate_json.get('notice_period')


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    job_positions = relationship("JobPosition", back_populates="project")

    def __init__(self, name=""):
        self.name = name

    @property
    def serialize(self):
        return {"name": self.name}


class JobPosition(Base):
    __tablename__ = "job_position"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    experience = Column(Integer, nullable=False)
    skills = Column(String(255), nullable=False)
    no_of_openings = Column(Integer, nullable=False, default=1)
    status = Column(String(30), nullable=False, default="OPEN")
    grade = Column(String(5), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"))
    employee_id = Column(Integer, ForeignKey("employee.id"))  # Hiring manager id

    project = relationship(Project, back_populates="job_positions", uselist=False)
    employee = relationship(Employee, back_populates="job_positions", uselist=False)

    def __init__(self, title, experience, skill, no_of_openings, status, grade):
        self.title = title
        self.experience = experience
        self.skills = skill
        self.no_of_openings = no_of_openings
        self.status = status
        self.grade = grade

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "experience": self.experience,
            "skills": self.skills,
            "no_of_openings": self.no_of_openings,
            "status": self.no_of_openings,
            "grade": self.grade,
            "employee_id":self.employee_id,
            "project_id":self.project_id
        }

    @property
    def deserialize(self, data):
        self.employee_id = data['employee_id']
        self.title = data['title']
        self.experience = data['experience']
        self.skills = data['skills']
        self.no_of_openings = data['no_of_openings']
        self.status = data['status']
        self.grade = data['grade']
        self.project_id = data['project_id']


class JobHasCandidate(Base):
    __tablename__ = "job_has_candidate"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidate.id"), default=0)
    position_id = Column(Integer, ForeignKey("job_position.id"), default=0)


class Interview(Base):
    __tablename__ = "interview"
    id = Column("id", Integer, primary_key=True)
    job_has_candidate_id = Column("job_has_candidate_id", Integer, ForeignKey('job_has_candidate.id'))
    employee_id = Column("employee_id", Integer, ForeignKey('employee.id'))
    channel = Column("channel", String(50))
    location = Column("location", String(50))
    comment = Column("comment", String(50), nullable=True)
    feedback = Column("feedback", String(50), nullable=True)
    schedule_time = Column("schedule_time", DateTime)
    job_has_candidate = relationship(JobHasCandidate, back_populates="interviews", uselist=False)
    employee = relationship(Employee, back_populates="interviews", uselist=False)

    def __init__(self, data, interview_id= None):
        if interview_id is not None:
            self.id = interview_id
        self.job_has_candidate_id = data["job_has_candidate_id"]
        self.employee_id = data["employee_id"]
        self.channel = data["channel"]
        self.location = data["location"]
        self.comment = data["comment"]
        self.feedback = data["feedback"]
        self.schedule_time = datetime.strptime(data["schedule_time"], "%d/%m/%Y, %H:%M:%S")

    def serialize(self):
        return {
            "id": self.id,
            "job_has_candidate_id": self.job_has_candidate_id,
            "employee_id": self.employee_id,
            "channel": self.channel,
            "location": self.location,
            "comment": self.comment,
            "feedback": self.feedback,
            "schedule_time": self.schedule_time,
        }

JobHasCandidate.interviews = relationship(Interview, order_by = Interview.id, back_populates="job_has_candidate", uselist=False)
Employee.interviews = relationship(Interview, order_by = Interview.id, back_populates="employee", uselist=False)


if __name__ == "__main__":
    # engine = create_engine(
    #     "sqlite:///ats.db", connect_args={"check_same_thread": False}, poolclass=StaticPool
    # )
    engine = create_engine("mysql+pymysql://dhruv:dhruv@localhost/ats")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()

    for a in session.query(Employee).all():
        print(a.serialize())
