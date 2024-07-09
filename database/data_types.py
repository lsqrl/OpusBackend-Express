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

class Users(Base):
    __tablename__ = 'users'
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
    #is_blocked = Column(String(2), nullable=False) # 'Y' or 'N'
    __table_args__ = (
        CheckConstraint(
            "role_id IN ('Provider', 'Taker', 'Both')",
            name='role_id_check'
        ),
        CheckConstraint(
            "age >= 18 AND age <= 99",
            name='age_check'
        ),
        CheckConstraint(
            "gender IN ( 'Male', 'Female', 'Non-binary', 'Other')",
            name='gender_check'
        )
    )

    child_lpt = relationship('LiquidityPoolTrans', back_populates='parent_user')
    
    child_lpa = relationship('LiquidityProviderAccountTrans', back_populates='parent_user')
    child_ma = relationship('MarginAccountTrans', back_populates='parent_user')
    
    child_tl = relationship('TradeLog', back_populates='parent_user')

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
    
class LiquidityProviderAccountTrans(Base):
    __tablename__ = 'liquidity_provider_account_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    parent_user = relationship('Users', back_populates='child_lpa')
    
    __table_args__ = (
        CheckConstraint("transaction_type IN ('internal_deposit', 'internal_withdrawal', 'external_deposit', 'external_withdrawal')", name='valid_transaction_type'),
    ) 
    
    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, bytes):  # Convert binary data to hex string
                value = value.hex()
            result[column.name] = value
        return result
    
    def __repr__(self):
        return (f"<LiquidityProviderAccountTrans(id={self.id}, user_id={self.user_id}, "
                f"transaction_type='{self.transaction_type}', amount={self.amount}, "
                f"timestamp='{self.timestamp}')>") 
    
class LiquidityPool(Base):
    __tablename__ = 'liquidity_pool'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    total_balance = Column(Float, nullable=False)
    total_shares = Column(Float, nullable=False)
    
    __table_args__ = (
        CheckConstraint('total_balance >= 0', name='positive_total_balance'),
        CheckConstraint('total_shares >= 0', name='positive_total_shares'),
    )

    parent_c = relationship('Currency', back_populates='child_lp')
    child_lpt = relationship('LiquidityPoolTrans', back_populates='parent_pool')
    
    def __repr__(self):
        return (f"<LiquidityPool(pool_id={self.pool_id}, currency_id='{self.currency_id}', "
                f"total_balance={self.total_balance}, total_shares={self.total_shares})>")

class LiquidityPoolTrans(Base):
    __tablename__ = 'liquidity_pool_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id')) # can be null
    pool_id = Column(Integer, ForeignKey('liquidity_pool.id'), nullable=False)
    user_shares = Column(Float)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        CheckConstraint("(transaction_type IN ('allocate', 'deallocate') AND user_id IS NOT NULL) OR transaction_type NOT IN ('allocate', 'deallocate')", name='user_id_required_for_allocate_deallocate'),
        CheckConstraint("(transaction_type = 'allocate' AND user_shares > 0) OR (transaction_type = 'deallocate' AND user_shares < 0) OR transaction_type NOT IN ('allocate', 'deallocate')", name='user_shares_sign'),
        CheckConstraint("(transaction_type = 'allocate' AND amount > 0) OR (transaction_type = 'deallocate' AND amount < 0) OR transaction_type NOT IN ('allocate', 'deallocate')", name='amount_sign')
    )

    parent_user = relationship('Users', back_populates='child_lpt')
    parent_pool = relationship('LiquidityPool', back_populates='child_lpt')

    def __repr__(self):
        return (f"<LiquidityPoolTrans(id={self.id}, pool_id={self.pool_id}, user_id={self.user_id}, "
                f"user_shares={self.user_shares}, transaction_type='{self.transaction_type}', "
                f"amount={self.amount}, timestamp='{self.timestamp}')>")


class MarginAccountTrans(Base):
    __tablename__ = 'margin_account_transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)

    parent_user = relationship('Users', back_populates='child_ma')

    def __repr__(self):
        return (f"<MarginAccountTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', margin_account_id='{self.margin_account_id}', amount={self.amount})>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Options(Base):
    __tablename__ = 'options'
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

    child_tl = relationship('TradeLog', back_populates='parent_op')

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
    option_id = Column(ForeignKey('options.id'))
    user_id = Column(ForeignKey('users.id'))

    parent_op = relationship('Options', back_populates='child_tl')
    parent_user = relationship('Users', back_populates='child_tl')

    def __repr__(self):
        return (f"<TradeLog(id={self.id}, timestamp='{self.timestamp}', "
                f"option_id='{self.option_id}', user_id='{self.user_id}')>") 

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}