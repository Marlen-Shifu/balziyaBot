from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///db.sqlite", echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'registered_users'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, unique=True)
    username = Column(String(255))


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    day = Column(String(12))
    time = Column(String(12))
    client = Column(String(255))
    aim = Column(String(255))


Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def add_user(id, username):
    s = get_session()

    try:
        new_user = User(id = id, username = username)
        s.add(new_user)

        s.commit()

    except Exception as e:
        print(e)


def add_record(day, time, client, aim):
    s = get_session()

    try:
        new_record = Record(day = day, time = time, client = client, aim = aim)
        s.add(new_record)

        s.commit()

        print(new_record)

    except Exception as e:
        print(e)