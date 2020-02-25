from _ast import For
from sys import meta_path
import json
import pymysql
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, Sequence, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import relationship, Session, sessionmaker


def create_connection():
    engine = None
    try:
        engine = create_engine("mysql+pymysql://root:QA@vnet1@localhost/ats")
        connection = engine.connect()
        print("Connection successful")
        return connection
    except Exception as e:
        print(e)
        print("Unable to create connection")

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    job_position = relationship("JobPosition", back_populates="project")

    def __init__(self, name):
        self.name = name

    def __init__(self):
        str = "abc"

    def serialize(self):
        return { 'id' : self.id,
                 'name' : self.name
                }

    def deserialize(self, reqJson):
        data = json.loads(reqJson)
        self.name = data['name']

class JobPosition(Base):
    __tablename__ = "job_position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    employee_id = Column(Integer, nullable=False)
    title = Column(String(50), nullable=False)
    experience = Column(Integer, nullable=False, default=0)
    skills = Column(String(255))
    no_of_openings = Column(Integer, nullable=False, default=0)
    status = Column(String(30))
    grade = Column(String(30), nullable=False)

    project = relationship("Project", back_populates="job_position", uselist = False)

    def __init__(self, employeeid, title, experience, skills, no_of_openings, status, grade ):
        self.employee_id = employeeid
        self.title = title
        self.experience = experience
        self.skills = skills
        self.no_of_openings = no_of_openings
        self.status = status
        self.grade = grade

    def __init__(self):
        str = "abc"

    def serialize(self):
        return {'id': self.id,
                'employee_id': self.employee_id,
                'title': self.title,
                'experience': self.experience,
                'skills': self.skills,
                'no_of_openings': self.no_of_openings,
                'status': self.status,
                'grade' : self.grade,
                'project_id' : self.project_id
                }

    def deserialize(self, data):
        self.employee_id = data['employee_id']
        self.title = data['title']
        self.experience = data['experience']
        self.skills = data['skills']
        self.no_of_openings = data['no_of_openings']
        self.status = data['status']
        self.grade = data['grade']
        self.project_id = data['project_id']

    def addPosition(self, session,reqJson):
        jobPosition = JobPosition()
        jobPosition.deserialize(reqJson)
        session.add(jobPosition)
        session.commit()
        return jobPosition
