from sqlalchemy import Column, CheckConstraint, Integer, LargeBinary, Float, String, DateTime, CheckConstraint, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base

# we need to make sure to establish relationships between different entities
# we should declare most of the tables immutable (maybe we need to have a timestamp for everything
# in the immutable case)
"""
# How to define foreign key

class Parent(Base):
...
    children = relationship('Child', back_populates='parent')

class Child(Base):
...
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship('Parent', back_populates='children')
"""

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    role_id = Column(String, nullable=False)
    wallet_address = Column(LargeBinary(20), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    kyc_aml_id = Column(LargeBinary(100), nullable=False)
    __table_args__ = (
        CheckConstraint(
            "role_id IN ('Provider', 'Taker', 'Both')",
            name='role_id_check'
        ),
        CheckConstraint(
            "age >= 18 AND age <= 99",
            name='age_check'
        )
    )

    child_lpt = relationship('LiquidityPoolTrans', back_populates='parent_user')
    child_ma = relationship('MarginAccount', back_populates='parent_user')

    def __repr__(self):
        return (f"<User(name='{self.name}', email='{self.email}', role_id='{self.role_id}', "
                f"wallet_address='{self.wallet_address.hex()}', age={self.age}, gender='{self.gender}')>")
    
    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, bytes):  # Convert binary data to hex string
                value = value.hex()
            result[column.name] = value
        return result
    
class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(8), nullable=False)

    child_lp = relationship('LiquidityPool', back_populates='parent_c')

    def __repr__(self):
        return f"<Currency(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LiquidityPool(Base):
    __tablename__ = 'liquidity_pool'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    balance = Column(Float, nullable=False)
    
    parent_c = relationship('Currency', back_populates='child_lp')
    child_lpt = relationship('LiquidityPoolTrans', back_populates='parent_pool')

    def __repr__(self):
        return f"<LiquidityPool(id={self.id}, currency_id='{self.currency_id}', balance={self.balance})>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LiquidityPoolTrans(Base):
    __tablename__ = 'liquidity_pool_trans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    pool_id = Column(Integer, ForeignKey('liquidity_pool.id'))
    amount = Column(Float, nullable=False)

    parent_user = relationship('User', back_populates='child_lpt')
    parent_pool = relationship('LiquidityPool', back_populates='child_lpt')

    def __repr__(self):
        return (f"<LiquidityPoolTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', pool_id='{self.pool_id}', amount={self.amount})>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MarginAccount(Base):
    __tablename__ = 'margin_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp_opening = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    parent_user = relationship('User', back_populates='child_ma')

    def __repr__(self):
        return (f"<MarginAccount(id={self.id}, timestamp_opening='{self.timestamp_opening}', "
                f"user_id='{self.user_id}')>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(100), nullable=False)
    maturity = Column(String, nullable=False)
    strike = Column(String, nullable=False)
    direction = Column(String(4), nullable=False)
    strategy = Column(String(4), nullable=False)
    premium = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    notional = Column(Float, nullable=False)
    __table_args__ = (
        CheckConstraint(
            "maturity IN ('1M', '2M', '3M', '6M', '1Y', 'Custom')",
            name='maturity_check'
        ),
        CheckConstraint(
            "strike IN ('ATM', 'Spot +-5%', 'Custom')",
            name='strike_check'
        ),
        CheckConstraint(
            "direction IN ('buy', 'sell')",
            name='direction_check'
        ),
        CheckConstraint(
            "strategy IN ('call', 'put')",
            name='strategy_check'
        )
    )

    def __repr__(self):
        return (f"<Option(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}', maturity='{self.maturity}', "
                f"strike={self.strike}, direction='{self.direction}', strategy='{self.strategy}', premium={self.premium}, "
                f"margin={self.margin}, notional={self.notional})>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TradeLog(Base):
    __tablename__ = 'trade_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    option_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<TradeLog(id={self.id}, timestamp='{self.timestamp}', "
                f"option_id='{self.option_id}', user_id='{self.user_id}')>") 

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

