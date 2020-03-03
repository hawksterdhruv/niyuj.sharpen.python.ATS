from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST="localhost"
USERNAME="root"
PASSWORD="tos1byte"
DATABASE="ats"

engine = create_engine("mysql+pymysql://"+USERNAME+":"+PASSWORD+"@"+HOST+"/"+DATABASE)
connection=engine.connect()
Session = sessionmaker(bind =engine)
session = Session()