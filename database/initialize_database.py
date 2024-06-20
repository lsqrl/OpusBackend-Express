from sqlalchemy import create_engine
from sqlalchemy import Table, Column, CheckConstraint, Integer, LargeBinary, Boolean, Float, String, DateTime, \
Text, ForeignKey, UniqueConstraint, CheckConstraint, Computed, MetaData
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




def demo_adding_user():
    # Example Usage: Add and Commit Data
    new_user = User(
        role_id='admin',
        wallet_address=b'\x00' * 20,  # Example 20-byte address
        name='John Doe',
        address='1234 Example Street, Example City, EX 12345',
        age=30,
        gender='Male',
        email='johndoe@example.com',
        kyc_aml_id=b'%PDF-1.4...'  # Example binary content for a PDF file
    )
    session.add(new_user)
    session.commit()

    # Example Usage: Query Data
    for user in session.query(User).order_by(User.id):
        print(user)

if __name__ == "__main__":
    init_database()
    demo_adding_user()