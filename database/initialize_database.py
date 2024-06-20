from sqlalchemy import create_engine
from sqlalchemy import Table, Column, CheckConstraint, Integer, LargeBinary, Boolean, Float, String, DateTime, \
Text, ForeignKey, UniqueConstraint, CheckConstraint, Computed, MetaData, func
from sqlalchemy.engine import URL
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, relationship, backref, sessionmaker
from datetime import datetime, timezone
import pandas as pd
import numpy as np
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()
connection = None
session = None

# probably we want to have a database and a schema per scenario we want to demo
url = URL.create(
    drivername="postgresql",
    username="",
    password="",
    host="localhost",
    port=5432,
    database="postgres"
)


def init_database():
    engine = create_engine(url)
    global connection
    connection = engine.connect()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    global session
    session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    role_id = Column(String, nullable=False)
    wallet_address = Column(LargeBinary(20), nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 18 AND age <= 99'), nullable=False)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    kyc_aml_id = Column(LargeBinary(100), nullable=False)

    def __repr__(self):
        return (f"<User(name='{self.name}', email='{self.email}', role_id='{self.role_id}', "
                f"wallet_address='{self.wallet_address.hex()}', age={self.age}, gender='{self.gender}')>")


if __name__ == "__main__":
    NUMBER_OF_USERS = 100
    init_database()
    # clear the table if it exists
    session.query(User).delete()
    session.commit()
    from data_faking_example import fake_user_table
    fake_user_table(session=session, num_rows=NUMBER_OF_USERS)
    # Check if the users were written
    for user in session.query(User).order_by(User.id):
        print(user)
    user_count = session.query(func.count(User.id)).scalar()
    print(f"Number of entries in the 'users' table: {user_count}")