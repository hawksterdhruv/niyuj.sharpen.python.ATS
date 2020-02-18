from sqlalchemy import Column, Integer, String, DateTime
from SetupDb import Base
import json
from datetime import datetime

class Interview(Base):
    __tablename__ = 'interview'
    id = Column('id', Integer, primary_key=True)
    job_has_candidate_id = Column('job_has_candidate_id', Integer) # ForeignKey('job_has_candidate.id')
    employee_id = Column('employee_id', Integer)  # ForeignKey('employee.id')
    channel = Column('channel', String(50))
    location = Column('location', String(50))
    comment = Column('comment', String(50), nullable=True)
    feedback = Column('feedback', String(50), nullable=True)
    schedule_time = Column('schedule_time', DateTime)

    # def __init__(self, job_has_candidate_id, employee_id, channel,location, comment, feedback, schedule_time):
    #     self.job_has_candidate_id = job_has_candidate_id
    #     self.employee_id = employee_id
    #     self.channel = channel
    #     self.location = location
    #     self.comment = comment
    #     self.feedback = feedback
    #     self.schedule_time = schedule_time

    def __init__(self, data):
        self.job_has_candidate_id = data['job_has_candidate_id']
        self.employee_id = data['employee_id']
        self.channel = data['channel']
        self.location = data['location']
        self.comment = data['comment']
        self.feedback = data['feedback']
        self.schedule_time = datetime.strptime(data['schedule_time'], '%m/%d/%y %H:%M:%S')


    def serialize(self):
        return {
            "id" : self.id,
            "job_has_candidate_id" : self.job_has_candidate_id,
            "employee_id" : self.employee_id,
            "channel" : self.channel ,
            "location" : self.location ,
            "comment" : self.comment ,
            "feedback" : self.feedback ,
            "schedule_time" : self.schedule_time
        }
