# this is our postgreSQL database 

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from server import app
import os
import psycopg2
import urlparse
#check to see if app is running in production or dev mode
is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    #Initialize postgreSQL genome database with appropriate database name, user, and password
    engine = create_engine('postgres://kcnqonukutmphz:GEyGV9nTZF0PJsxBN6yVxQSOMH@ec2-54-83-198-111.compute-1.amazonaws.com:5432/d6famvj5mosmlf', convert_unicode=True)
else:
    engine = create_engine('postgres://localhost/mysite_development', convert_unicode=True)
    try:
        #connect to database if it exissts
        connection = connect(dbname='mysite_development', user='tunnelsup', host='localhost', password='mala')
    except:
        #create database if it does not already exist
        connection = connect(user='tunnelsup', host='localhost', password='mala')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE mysite_development")
        cursor.close()
        connection.close()

        # what is session maker?

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session_factory)
Base = declarative_base()
Base.query = db_session.query_property()



#User model Schema
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, unique=True)
    
    
    profile_id = Column(String(255))
    first_name = Column(String(255))
    rs761100 = Column(String(255), nullable=True)
    rs12340895 = Column(String(255), nullable=True)
    rs10488631 = Column(String(255), nullable=True)
    rs2287622 = Column(String(255), nullable=True)
    rs3803662 = Column(String(255), nullable=True)
    rs1219648 = Column(String(255), nullable=True)
    rs6025 = Column(String(255), nullable=True)
    rs6457617 = Column(String(255), nullable=True)
    rs3923809 = Column(String(255), nullable=True)
    rs1061147 = Column(String(255), nullable=True)
    rs1805007 = Column(String(255), nullable=True)
    rs2165241 = Column(String(255), nullable=True)
    rs2395185 = Column(String(255), nullable=True)
    rs9273363 = Column(String(255), nullable=True)
    rs2187668 = Column(String(255), nullable=True)
    rs2066844 = Column(String(255), nullable=True)
    rs2200733 = Column(String(255), nullable=True)
    rs1064395 = Column(String(255), nullable=True)
    rs10995190 = Column(String(255), nullable=True)
    rs7524102 = Column(String(255), nullable=True)
    rs2235529 = Column(String(255), nullable=True)
    rs7754840 = Column(String(255), nullable=True)
    rs7850258 = Column(String(255), nullable=True)
    

    def __init__(self, profile_id, first_name, genotype_info):
        self.profile_id = profile_id
        self.first_name = first_name
        self.rs761100 = genotype_info['rs761100']
        self.rs12340895 = genotype_info['rs12340895']
        self.rs10488631 = genotype_info['rs10488631']
        self.rs2287622 = genotype_info['rs2287622']
        self.rs3803662 = genotype_info['rs3803662']
        self.rs1219648 = genotype_info['rs1219648']
        self.rs6025 = genotype_info['rs6025']
        self.rs6457617 = genotype_info['rs6457617']
        self.rs3923809 = genotype_info['rs3923809']
        self.rs1061147 = genotype_info['rs1061147']
        self.rs1805007 = genotype_info['rs1805007']
        self.rs2165241 = genotype_info['rs2165241']
        self.rs2395185 = genotype_info['rs2395185']
        self.rs9273363 = genotype_info['rs9273363']
        self.rs2187668 = genotype_info['rs2187668']
        self.rs2066844 = genotype_info['rs2066844']
        self.rs2200733 = genotype_info['rs2200733']
        self.rs1064395 = genotype_info['rs1064395']
        self.rs10995190 = genotype_info['rs10995190']
        self.rs7524102 = genotype_info['rs7524102']
        self.rs2235529 = genotype_info['rs2235529']
        self.rs7754840 = genotype_info['rs7754840']
        self.rs7850258 = genotype_info['rs7850258']
       

    def serialize(self):
        return {
            'profile_id': self.profile_id,
            'first_name': self.first_name,
            'rs761100': self.rs761100,
            'rs12340895': self.rs12340895,
            'rs10488631': self.rs10488631,
            'rs2287622': self.rs2287622,
            'rs3803662': self.rs3803662,
            'rs1219648': self.rs1219648, 
            'rs6025': self.rs6025, 
            'rs6457617': self.rs6457617, 
            'rs3923809': self.rs3923809,
            'rs1061147': self.rs1061147, 
            'rs1805007': self.rs1805007, 
            'rs2165241': self.rs2165241,
            'rs2395185': self.rs2395185, 
            'rs9273363': self.rs9273363, 
            'rs2187668': self.rs2187668, 
            'rs2066844': self.rs2066844, 
            'rs2200733': self.rs2200733, 
            'rs1064395': self.rs1064395, 
            'rs10995190': self.rs10995190, 
            'rs7524102': self.rs7524102, 
            'rs2235529': self.rs2235529, 
            'rs7754840': self.rs7754840, 
            'rs7850258': self.rs7850258
        
        }

  





#Snp data schema
class Snp(Base):
    __tablename__ = 'snps'
    id = Column(Integer(), primary_key=True, unique=True)

    title = Column(String(255))
    rsid = Column(String(255))
    pair = Column(String(255))
    outcome = Column(String(255))
    r = Column(String(225))
    healthtip = Column(String(1000))

    def __init__(self, title, rsid, pair, outcome, r, healthtip):
        self.title = title
        self.rsid = rsid
        self.pair = pair
        self.outcome = outcome
        self.r = r
        self.healthtip = healthtip

       


    def serialize(self):
        return {
            'title': self.title,
            'rsid': self.rsid,
            'pair': self.pair,
            'outcome': self.outcome,
            'r': self.r,
            'healthtip': self.healthtip
          
        }


Base.metadata.create_all(engine)