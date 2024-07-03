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
    password = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 18 AND age <= 99'), nullable=False)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    kyc_aml_id = Column(LargeBinary(100), nullable=False)

    def __repr__(self):
        return (f"<User(name='{self.name}', email='{self.email}', role_id='{self.role_id}', "
                f"wallet_address='{self.wallet_address.hex()}', age={self.age}, gender='{self.gender}')>")
    
    
class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(8), nullable=False)

    def __repr__(self):
        return f"<Currency(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"

class LiquidityPool(Base):
    __tablename__ = 'liquidity_pool'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<LiquidityPool(id={self.id}, currency_id='{self.currency_id}', balance={self.balance})>"


class LiquidityPoolTrans(Base):
    __tablename__ = 'liquidity_pool_trans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(String(100), nullable=False)
    pool_id = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<LiquidityPoolTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', pool_id='{self.pool_id}', amount={self.amount})>")


class MarginAccount(Base):
    __tablename__ = 'margin_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp_opening = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<MarginAccount(id={self.id}, timestamp_opening='{self.timestamp_opening}', "
                f"user_id='{self.user_id}')>")

class MarginAccountTrans(Base):
    __tablename__ = 'margin_account_trans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(String(100), nullable=False)
    margin_account_id = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<MarginAccountTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', margin_account_id='{self.margin_account_id}', amount={self.amount})>")

class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(100), nullable=False)
    maturity = Column(DateTime, nullable=False)    # 1M, 2M, 3M, 6M, 1Y, Custom
    strike = Column(Float, nullable=False)         # ATM, Spot +-5%, Custom
    direction = Column(String(4), nullable=False)  # "buy" or "sell"
    strategy = Column(String(4), nullable=False)       # "call" or "put"
    premium = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    notional = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<Option(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}', maturity='{self.maturity}', "
                f"strike={self.strike}, direction='{self.direction}', strategy='{self.strategy}', premium={self.premium}, "
                f"margin={self.margin}, notional={self.notional})>")

class TradeLog(Base):
    __tablename__ = 'trade_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    option_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<TradeLog(id={self.id}, timestamp='{self.timestamp}', "
                f"option_id='{self.option_id}', user_id='{self.user_id}')>") 


if __name__ == "__main__":
    NUMBER_OF_USERS = 100
    NUMBER_OF_POOLS = 10
    init_database()
    # clear the table if it exists
    session.query(User).delete()
    session.commit()
    from data_faking_example import *
    fake_user_table(session=session, num_rows=NUMBER_OF_USERS)
    fake_currency_table(session=session)
    fake_liquidity_pool_table(session=session, num_pools=NUMBER_OF_POOLS)
    # Check if the users were written
    for user in session.query(User).order_by(User.id):
        print(user)
    user_count = session.query(func.count(User.id)).scalar()
    print(f"Number of entries in the 'users' table: {user_count}")