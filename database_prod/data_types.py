from sqlalchemy import Column, CheckConstraint, UniqueConstraint, Integer, BigInteger, \
    LargeBinary, Float, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base()

# Define metadata for each schema
schema_old = 'old'
schema_counterparty = 'counterparty'
schema_account = 'account'
schema_funding_sources = 'funding_sources'
schema_deposits = 'deposits'
schema_trades = 'trades'
schema_funding = 'funding'
schema_market_data_system = 'market_data_system'

# Step 0: define all the tables
# Step 1: define all the column constraints via table args next to schema name
# Step 2: connect all the keys
# Step 3: generate fake values
# Step 4: connect via API to web UI
# Step 5: have different databases for different scenario showcasing in the MVP

# Defining the new entities

class Retail(Base):
    __tablename__ = 'retail'
    __table_args__ = (
        CheckConstraint(
            "gender IN ('Male', 'Female', 'Non-binary', 'Other')",
            name='gender_check'
        ),
        {'schema': schema_counterparty}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    onboarding_datetime = Column(DateTime, nullable=False)
    email = Column(String(254), nullable=False, unique=True)
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
                f"telephone_number={self.telephone_number}, "
                "address_of_residence={self.address_of_residence}, "
                f"country_of_residence={self.country_of_residence}, "
                "citizenship={self.citizenship}, "
                f"gender={self.gender}, birth_date={self.birth_date}, "
                "ssn={self.ssn}, dossier_id={self.dossier_id})>")

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
    __table_args__ = (
        {'schema': schema_counterparty}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    legal_entity_name = Column(String(500), nullable=False)
    onboarding_datetime = Column(DateTime, nullable=False)
    email = Column(String(254), nullable=False, unique=True)
    telephone_number = Column(String(100), nullable=False)
    legal_address = Column(String(300), nullable=False)
    country_of_incorporation = Column(String(200), nullable=False)
    dossier_id = Column(String(50), nullable=False)

    def __repr__(self):
        return (f"<LegalEntity(id={self.id}, "
                "legal_entity_name={self.legal_entity_name}, "
                "email={self.email}, "
                f"telephone_number={self.telephone_number}, "
                "legal_address={self.legal_address}, "
                f"country_of_incorporation={self.country_of_incorporation}, "
                "dossier_id={self.dossier_id})>")

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
    __table_args__ = (
        CheckConstraint(
            "name IN ('Depositor', 'System')",
            name='account_check'
        ),
        {'schema': schema_account}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    
    child_at = relationship('Account',
                             back_populates='parent_a')

    def __repr__(self):
        return f"<AccountType(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Currencies(Base):
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
    chain_id = Column(BigInteger, nullable=True) # Solana has no ID
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
    type_id = Column(Integer, ForeignKey('account.account_types.id'))
    opening_time = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    closing_time = Column(DateTime, nullable=False,
                          default=datetime(2999, 12, 31, 0, 0))
    trade_enabled = Column(Boolean, nullable=False, default=True)

    parent_a = relationship('AccountType', back_populates='child_at')


    def __repr__(self):
        return (f"<Account(id={self.id}, counterparty_id={self.counterparty_id}, "
                f"counterparty_type='{
                    self.counterparty_type}', type_id={self.type_id}, "
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
"""
Given the fact that there are 2 options for counterparties, we need to be able to handle polymorphic relaitonship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)  # This could be a User ID or an Organization ID
    entity_type = Column(String)  # This indicates which table the entity_id refers to

    # Polymorphic relationship
    @property
    def entity(self):
        if self.entity_type == 'user':
            return self.session.query(User).filter_by(id=self.entity_id).first()
        elif self.entity_type == 'organization':
            return self.session.query(Organization).filter_by(id=self.entity_id).first()

# Setup database (in-memory SQLite for example purposes)
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example usage
user = User(name='John Doe')
organization = Organization(name='Acme Inc.')
activity1 = Activity(entity_id=1, entity_type='user')
activity2 = Activity(entity_id=1, entity_type='organization')

session.add(user)
session.add(organization)
session.add(activity1)
session.add(activity2)
session.commit()

# Accessing the entity
for activity in session.query(Activity).all():
    print(activity.entity)


"""

class Wallet(Base):
    __tablename__ = 'wallets'
    __table_args__ = {'schema': schema_funding_sources}
    id = Column(Integer, primary_key=True, autoincrement=True)

class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    __table_args__ = {'schema': schema_funding_sources}
    id = Column(Integer, primary_key=True, autoincrement=True)

class BankDeposit(Base):
    __tablename__ = 'bank_deposits'
    __table_args__ = {'schema': schema_deposits}
    id = Column(Integer, primary_key=True, autoincrement=True)

class CryptoDeposit(Base):
    __tablename__ = 'crypto_deposits'
    __table_args__ = {'schema': schema_deposits}
    id = Column(Integer, primary_key=True, autoincrement=True)

class TradeType(Base):
    __tablename__ = 'trade_types'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)
    
class Instrument(Base):
    __tablename__ = 'instruments'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)
    
class Portfolio(Base):
    __tablename__ = 'portfolios'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class TradeToPortfolio(Base):
    __tablename__ = 'trade_to_portfolio'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class FundingFromFiat(Base):
    __tablename__ = 'funding_from_fiat'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class FundingFromCrypto(Base):
    __tablename__ = 'funding_from_crypto'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class Loans(Base):
    __tablename__ = 'loans'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class FXSpot(Base):
    __tablename__ = 'fx_spot'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class CryptoSpot(Base):
    __tablename__ = 'crypto_spot'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class CryptoPerpetual(Base):
    __tablename__ = 'crypto_perpetual'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class FiatOptions(Base):
    __tablename__ = 'fiat_options'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

class CryptoOptions(Base):
    __tablename__ = 'crypto_options'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)

"""
We will need a junction table to associate tradeIDs to portfolios
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Define the junction table
enrollment_table = Table(
    'enrollments', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

# Define the Student model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the relationship to the Course model via the junction table
    courses = relationship('Course', secondary=enrollment_table, back_populates='students')

# Define the Course model
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the relationship to the Student model via the junction table
    students = relationship('Student', secondary=enrollment_table, back_populates='courses')

    Session = sessionmaker(bind=engine)

session = Session()

# Create some students and courses
student1 = Student(name='Alice')
student2 = Student(name='Bob')

course1 = Course(name='Math')
course2 = Course(name='History')

# Establish relationships
student1.courses.append(course1)
student1.courses.append(course2)
student2.courses.append(course1)

# Add and commit to the database
session.add(student1)
session.add(student2)
session.commit()

# Query the relationships
for student in session.query(Student).all():
    print(f"Student: {student.name}")
    for course in student.courses:
        print(f"Enrolled in: {course.name}")

"""


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registered_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    role_id = Column(String, nullable=False)
    wallet_address = Column(LargeBinary(20), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    kyc_aml_id = Column(LargeBinary(100), nullable=False)
    # is_blocked = Column(String(2), nullable=False) # 'Y' or 'N'
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
        ),
        {'schema': schema_old}
    )

    child_lpt = relationship('LiquidityPoolTrans',
                             back_populates='parent_user')

    child_lpa = relationship(
        'LiquidityProviderAccountTrans', back_populates='parent_user')
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
    __table_args__ = {'schema': schema_old}
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
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('internal_deposit', 'internal_withdrawal', 'external_deposit', 'external_withdrawal')", 
            name='valid_transaction_type'),
        {'schema': schema_old}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('old.users.id'))
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)

    parent_user = relationship('Users', back_populates='child_lpa')

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
                f"transaction_type='{
                    self.transaction_type}', amount={self.amount}, "
                f"timestamp='{self.timestamp}')>")


class LiquidityPool(Base):
    __tablename__ = 'liquidity_pool'
    __table_args__ = {'schema': schema_old}

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey('old.currency.id'))

    parent_c = relationship('Currency', back_populates='child_lp')
    child_lpt = relationship('LiquidityPoolTrans',
                             back_populates='parent_pool')

    def __repr__(self):
        return (f"<LiquidityPool(pool_id={self.pool_id}, currency_id='{self.currency_id}'")


class LiquidityPoolTrans(Base):
    __tablename__ = 'liquidity_pool_transactions'
    __table_args__ = (
        CheckConstraint("(transaction_type IN ('allocate', 'deallocate') AND user_id IS NOT NULL) OR transaction_type NOT IN ('allocate', 'deallocate')",
                        name='user_id_required_for_allocate_deallocate'),
        CheckConstraint("(transaction_type = 'allocate' AND user_shares > 0) OR (transaction_type = 'deallocate' AND user_shares < 0) OR transaction_type NOT IN ('allocate', 'deallocate')", name='user_shares_sign'),
        CheckConstraint("(transaction_type = 'allocate' AND amount > 0) OR (transaction_type = 'deallocate' AND amount < 0) OR transaction_type NOT IN ('allocate', 'deallocate')", name='amount_sign'),
        {'schema': schema_old}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('old.users.id'))  # can be null
    pool_id = Column(Integer, ForeignKey('old.liquidity_pool.id'), nullable=False)
    user_shares = Column(Float)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)

    parent_user = relationship('Users', back_populates='child_lpt')
    parent_pool = relationship('LiquidityPool', back_populates='child_lpt')

    def __repr__(self):
        return (f"<LiquidityPoolTrans(id={self.id}, pool_id={self.pool_id}, user_id={self.user_id}, "
                f"user_shares={self.user_shares}, transaction_type='{
                    self.transaction_type}', "
                f"amount={self.amount}, timestamp='{self.timestamp}')>")


class MarginAccountTrans(Base):
    __tablename__ = 'margin_account_transactions'
    __table_args__ = {'schema': schema_old}
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey('old.users.id'))
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
        ),
        {'schema': schema_old}
    )

    child_tl = relationship('TradeLog', back_populates='parent_op')

    def __repr__(self):
        return (f"<Option(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}', maturity='{self.maturity}', "
                f"strike={self.strike}, direction='{self.direction}', strategy='{
                    self.strategy}', premium={self.premium}, "
                f"margin={self.margin}, notional={self.notional})>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TradeLog(Base):
    __tablename__ = 'trade_log'
    __table_args__ = {'schema': schema_old}
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    option_id = Column(ForeignKey('old.options.id'))
    user_id = Column(ForeignKey('old.users.id'))

    parent_op = relationship('Options', back_populates='child_tl')
    parent_user = relationship('Users', back_populates='child_tl')

    def __repr__(self):
        return (f"<TradeLog(id={self.id}, timestamp='{self.timestamp}', "
                f"option_id='{self.option_id}', user_id='{self.user_id}')>")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
