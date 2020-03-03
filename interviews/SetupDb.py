from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base

#create user 'ats-user'@'localhost' IDENTIFIED BY 'Abcdefg@123'
engine = create_engine('mysql+pymysql://root:tos1byte@localhost/ats', convert_unicode=True)
#engine = create_engine('sqlite:///ats.db', convert_unicode=True)

#engine = create_engine('mysql+pymysql://ats-user:Abcdefg@123@localhost/ats', convert_unicode=True)
#engine = create_engine('sqlite:///ats.db', convert_unicode=True)
# Base = declarative_base()


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    print("Crating db tables")
    Base.metadata.create_all(bind=engine)
