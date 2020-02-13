from sqlalchemy import Column, Integer, String, Text, BLOB, ForeignKey, create_engine, select
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from flaskext.jsontools import JsonSerializableBase
from flask import json,jsonify
from app import app

engine = create_engine("mysql+pymysql://root:user@123@localhost:3306/ats")
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

    #Relationship
    #reference = relationship("Employee",back_populates="candidate")

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


#Employee.candidate = relationship("Candidate", back_populates="reference")


'''
e=Employee("xyz","xyz@niyuj.com","Pune","7896504329")
session.add(e)
session.commit()

e=session.query(Employee).first()
#print(e.id)

c1= Candidate("ABC","java,c,cpp",3,"abc@gmail.com","Pune","9087650987","referral",e.id,bytes(json.dumps("/home/user1/PycharmProjects/ats/a.txt"), 'utf8'),"Shortlisted",4,6,"niyuj",15)
c2= Candidate("Shyamlee","c,cpp",5,"shyamlee@gmail.com","Pune","8907654908","referral",e.id,bytes(json.dumps("/home/user1/PycharmProjects/ats/a.txt"), 'utf8'),"Selected",7,10,"niyuj",10)
#c2.referred_by=e.id
session.add(c1)
session.add(c2)
session.commit()
'''

@app.route('/all',methods=["GET", "POST"])
def Show():
    try:
        select = session.query(Candidate).all()
        for emp in select:
            print({emp.id, emp.name, emp.email, emp.address, emp.mobileno})
        return ""
    except Exception as e:
      print(e)



if __name__ == "__main__":
    app.run()
