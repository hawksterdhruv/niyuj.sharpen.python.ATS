from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host="localhost"
port="3306"
username="root"
passwd="user@123"
dbname="ats"

engine = create_engine("mysql+pymysql://"+username+":"+passwd+"@"+host+":"+port+"/"+dbname)
connection=engine.connect()
Session = sessionmaker(bind =engine)
session = Session()