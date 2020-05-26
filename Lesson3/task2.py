from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def ListVacancySalary(session, MinSalary=0, MaxSalary=0 ):
    for vac in session.query(Vacancy).filter(Vacancy.minsalary > MinSalary):
        print(vac.name, vac.compensation, vac.link)


engine = create_engine('sqlite:///vacancies.db',echo=True)
Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    key = Column(String)
    name = Column(String)
    link = Column(String)
    host = Column(String)
    compensation = Column(String)
    minsalary = Column(Integer)
    maxsalary = Column(Integer)
    currency = Column(String)

    def __init__(self, key, name, link, host, compensation, minsalary, maxsalary, currency):
        self.key = key
        self.name = name
        self.link = link
        self.host = host
        self.compensation = compensation
        self.minsalary = minsalary
        self.maxsalary = maxsalary
        self.currency = currency


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

ListVacancySalary(session,100000)

session.commit()
session.close()