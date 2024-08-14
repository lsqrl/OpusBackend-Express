from sqlalchemy import Column, CheckConstraint, Integer, BigInteger, LargeBinary, Float, String, Boolean, Date, DateTime, CheckConstraint, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base()

# Define metadata for each schema
schema_counterparty = MetaData(schema='counterparty')
schema_account = MetaData(schema='account')
schema_funding_sources = MetaData(schema='funding_sources')
schema_deposits = MetaData(schema='deposits')
schema_trades = MetaData(schema='trades')
schema_funding = MetaData(schema='funding')
schema_market_data_system = MetaData(schema='market_data_system')

# State: generated classes for 1st and 2nd schemas

# Step 0: define all the tables
# Step 1: define all the column constraints
# Step 2: connect all the keys
# Step 3: generate fake values
# Step 4: connect via API to web UI
# Step 5: have different databases for different scenario showcasing in the MVP

# Defining the new entities
class Retial(Base):
    __tablename__ = 'retail'
    __table_args__ = {'schema': schema_counterparty}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    onboarding_datetime = Column(DateTime, nullable=False)
    email = Column(String(254), nullable=False)
    telephone_number = Column(String(100), nullable=False)
    address_of_residence = Column(String(300), nullable=False)
    country_of_residence = Column(String(200), nullable=False)
    citizenship = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=False)
    birth_date = Column(Date, nullable=False)
    ssn = Column(String(50), nullable=False)
    dossier_id = Column(String(50), nullable=False)
    
    def __repr__(self):
        return (f"<Person(id={self.id}, name={self.name}, email={self.email}, "
                f"telephone_number={self.telephone_number}, address_of_residence={self.address_of_residence}, "
                f"country_of_residence={self.country_of_residence}, citizenship={self.citizenship}, "
                f"gender={self.gender}, birth_date={self.birth_date}, ssn={self.ssn}, dossier_id={self.dossier_id})>")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'onboarding_datetime': self.onboarding_datetime,
            'email': self.email,
            'telephone_number': self.telephone_number,
            'address_of_residence': self.address_of_residence,
            'country_of_residence': self.country_of_residence,
            'citizenship': self.citizenship,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'ssn': self.ssn,
            'dossier_id': self.dossier_id
        }

class LegalEntity(Base):
    __tablename__ = 'legal_entities'
    __table_args__ = {'schema': schema_counterparty}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    legal_entity_name = Column(String(500), nullable=False)
    onboarding_datetime = Column(DateTime, nullable=False)
    email = Column(String(254), nullable=False)
    telephone_number = Column(String(100), nullable=False)
    legal_address = Column(String(300), nullable=False)
    country_of_incorporation = Column(String(200), nullable=False)
    dossier_id = Column(String(50), nullable=False)
    
    def __repr__(self):
        return (f"<LegalEntity(id={self.id}, legal_entity_name={self.legal_entity_name}, email={self.email}, "
                f"telephone_number={self.telephone_number}, legal_address={self.legal_address}, "
                f"country_of_incorporation={self.country_of_incorporation}, dossier_id={self.dossier_id})>")
    
    def to_dict(self):
        return {
            'id': self.id,
            'legal_entity_name': self.legal_entity_name,
            'onboarding_datetime': self.onboarding_datetime,
            'email': self.email,
            'telephone_number': self.telephone_number,
            'legal_address': self.legal_address,
            'country_of_incorporation': self.country_of_incorporation,
            'dossier_id': self.dossier_id
        }

class AccountType(Base):
    __tablename__ = 'account_types'
    __table_args__ = {'schema': schema_account}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<AccountType(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
class Currency(Base):
    __tablename__ = 'currencies'
    __table_args__ = {'schema': schema_account}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    trad_fi = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Currencies(id={self.id}, name='{self.name}', trad_fi={self.trad_fi})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'trad_fi': self.trad_fi,
        }
    
class Chain(Base):
    __tablename__ = 'chains'
    __table_args__ = {'schema': schema_account}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    chain_id = Column(BigInteger, nullable=False)
    url = Column(String(500), nullable=False)

    def __repr__(self):
        return f"<Chain(id={self.id}, name='{self.name}', chain_id={self.chain_id}, url='{self.url}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'chain_id': self.chain_id,
            'url': self.url,
        }
    
class Account(Base):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': schema_account}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    counterparty_id = Column(Integer, nullable=False)
    counterparty_type = Column(String(30), nullable=False)
    type_id = Column(Integer, nullable=False)
    opening_time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    closing_time = Column(DateTime, nullable=False, default=datetime(2999, 12, 31, 0, 0))
    trade_enabled = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return (f"<Account(id={self.id}, counterparty_id={self.counterparty_id}, "
                f"counterparty_type='{self.counterparty_type}', type_id={self.type_id}, "
                f"opening_time='{self.opening_time}', active={self.active}, "
                f"closing_time='{self.closing_time}', trade_enabled={self.trade_enabled})>")

    def to_dict(self):
        return {
            'id': self.id,
            'counterparty_id': self.counterparty_id,
            'counterparty_type': self.counterparty_type,
            'type_id': self.type_id,
            'opening_time': self.opening_time,
            'active': self.active,
            'closing_time': self.closing_time,
            'trade_enabled': self.trade_enabled,
        }

# Example usage:

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
    
    parent_c = relationship('Currency', back_populates='child_lp')
    child_lpt = relationship('LiquidityPoolTrans', back_populates='parent_pool')
    
    def __repr__(self):
        return (f"<LiquidityPool(pool_id={self.pool_id}, currency_id='{self.currency_id}'")

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