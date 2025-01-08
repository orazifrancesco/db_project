from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as orm
from url import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

Base = orm.declarative_base()

def get_session():
    return Session()