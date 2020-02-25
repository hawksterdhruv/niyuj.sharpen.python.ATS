from datetime import datetime
from pprint import pprint

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import json

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# from model import *
Base = declarative_base()


# class BaseModel(Base):
#     __abstract__ = True
#     ignore_field = ['get_or_create', 'ignore_field','serialize']

#     @classmethod
#     def get_or_create(cls, sess,  **kwargs):
#         instance = sess.query(cls).filter_by(**kwargs).first()

#         if instance:
#             return instance, False
#         else:
#             instance = cls(**kwargs)
#             sess.add(instance)
#             return instance, True

#     def serialize(self):
#         fields = {}
#         for field in [x for x in dir(self) if not x.startswith('_') and x != 'metadata']:
#             if field in self.ignore_field:
#                 continue
#             data = self.__getattribute__(field)
#             try:
#                 if isinstance(data, datetime):
#                     data = data.strftime('%Y-%m-%d')
#                 json.dumps(data)  # this will fail on non-encodable values, like other classes
#                 fields[field] = data
#             except TypeError:
#                 try:
#                     json.dumps(data.name)  # this will fail on non-encodable values, like other classes
#                     fields[field] = data.name
#                 except TypeError:
#                     print(type(data))
#                     fields[field] = None

#         return fields


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    mobileno = Column(String(200), nullable=False)
    job_positions = relationship("JobPosition", back_populates="employee")

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
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    skills = Column(String(200), nullable=False)
    experience = Column(Integer, nullable=False)
    email = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    mobileno = Column(String(200), nullable=False)
    source = Column(String(200), nullable=False)
    refered_by = Column(Integer, ForeignKey("employee.id"), default=0)
    resume = Column(String(200), nullable=False)
    status = Column(String(200), nullable=False)
    current_ctc = Column(Integer, nullable=False)
    expected_ctc = Column(Integer, nullable=False)
    current_organization = Column(String(200), nullable=False)
    notice_period = Column(Integer, default=0)

    # def add_data(self, input_json):
    # self.ldjfl = input_json['key']


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
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    experience = Column(Integer, nullable=False)
    skills = Column(String(200), nullable=False)
    no_of_openings = Column(Integer, nullable=False, default=1)
    status = Column(String(200), nullable=False, default="OPEN")
    grade = Column(String(200), nullable=False)
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
            "title": self.title,
            "experience": self.experience,
            "skills": self.skills,
            "no_of_openings": self.no_of_openings,
            "status": self.no_of_openings,
            "grade": self.grade,
        }


class JobHasCandidate(Base):
    __tablename__ = "job_has_candidate"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidate.id"), default=0)
    position_id = Column(Integer, ForeignKey("job_position.id"), default=0)


class Interview(Base):
    __tablename__ = "interview"
    id = Column("id", Integer, primary_key=True)
    job_has_candidate_id = Column(
        "job_has_candidate_id", Integer
    )  # ForeignKey('job_has_candidate.id')
    employee_id = Column("employee_id", Integer)  # ForeignKey('employee.id')
    channel = Column("channel", String(50))
    location = Column("location", String(50))
    comment = Column("comment", String(50), nullable=True)
    feedback = Column("feedback", String(50), nullable=True)
    schedule_time = Column("schedule_time", DateTime)

    # def __init__(self, job_has_candidate_id, employee_id, channel,location, comment, feedback, schedule_time):
    #     self.job_has_candidate_id = job_has_candidate_id
    #     self.employee_id = employee_id
    #     self.channel = channel
    #     self.location = location
    #     self.comment = comment
    #     self.feedback = feedback
    #     self.schedule_time = schedule_time

    def __init__(self, data):
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
