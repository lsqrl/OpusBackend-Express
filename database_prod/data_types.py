from sqlalchemy import Table, Column, CheckConstraint, Integer, BigInteger, \
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
    onboarding_datetime = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
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

class Institutional(Base):
    __tablename__ = 'institutional'
    __table_args__ = (
        {'schema': schema_counterparty}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    legal_entity_name = Column(String(500), nullable=False)
    onboarding_datetime = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
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
            name='account_type_check'
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

    child_bd = relationship('BankDeposit',
                             back_populates='parent_c')
    child_cd = relationship('CryptoDeposit',
                             back_populates='parent_c')

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

    child_w = relationship('Wallet',
                             back_populates='parent_c')

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
    __table_args__ = (
        CheckConstraint(
            "counterparty_type IN ('Retail', 'Institutional')",
            name='account_check'
        ),
        {'schema': schema_account}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    counterparty_id = Column(Integer, nullable=False) # reference depends on counterparty_type
    counterparty_type = Column(String, nullable=False) # limited to counterparty tables
    type_id = Column(Integer, ForeignKey('account.account_types.id'))
    opening_time = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    closing_time = Column(DateTime, nullable=False,
                          default=datetime(2999, 12, 31, 0, 0))
    trade_enabled = Column(Boolean, nullable=False, default=True)

    parent_a = relationship('AccountType', back_populates='child_at')

    # Polymorphic relationship
    @property
    def entity(self):
        if self.counterparty_type == 'Retail':
            return self.session.query(Retail).filter_by(id=self.counterparty_id).first()
        elif self.counterparty_type == 'Institutional':
            return self.session.query(Institutional).filter_by(id=self.counterparty_id).first()

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

class Wallet(Base):
    __tablename__ = 'wallets'
    __table_args__ = (
        CheckConstraint(
            "counterparty_type IN ('Retail', 'Institutional')",
            name='account_check'
        ),
        {'schema': schema_funding_sources}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    counterparty_id = Column(Integer, nullable=False) # reference depends on counterparty_type
    counterparty_type = Column(String, nullable=False) # limited to counterparty tables
    address = Column(LargeBinary(20), nullable=False)
    chain_id = Column(Integer, ForeignKey('account.chains.id'), nullable=False)
    onboarding_timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)

    parent_c = relationship('Chain', back_populates='child_w')
    child_cd = relationship('CryptoDeposit',
                             back_populates='parent_w')
    
    # Polymorphic relationship
    @property
    def entity(self):
        if self.counterparty_type == 'Retail':
            return self.session.query(Retail).filter_by(id=self.counterparty_id).first()
        elif self.counterparty_type == 'Institutional':
            return self.session.query(Institutional).filter_by(id=self.counterparty_id).first()

    def __repr__(self):
        return (f"<Wallet(id={self.id}, counterparty_id={self.counterparty_id}, "
                f"counterparty_type='{self.counterparty_type}', address={self.address.hex()}, "
                f"chain_id={self.chain_id}, onboarding_timestamp={self.onboarding_timestamp})>")

    def to_dict(self):
        return {
            'id': self.id,
            'counterparty_id': self.counterparty_id,
            'counterparty_type': self.counterparty_type,
            'address': self.address.hex(),
            'chain_id': self.chain_id,
            'onboarding_timestamp': self.onboarding_timestamp.isoformat() if self.onboarding_timestamp else None
        }

class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    __table_args__ = {'schema': schema_funding_sources}
    id = Column(Integer, primary_key=True, autoincrement=True)
    counterparty_id = Column(Integer, nullable=False) # reference depends on counterparty_type
    counterparty_type = Column(String, nullable=False) # limited to counterparty tables
    number = Column(BigInteger, nullable=False)
    bank_name = Column(String(300), nullable=False)
    bank_address = Column(String(300), nullable=False)
    swift_bic_code = Column(String(50), nullable=False)
    iban = Column(String(50), nullable=False)
    onboarding_timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    
    child_bd = relationship('BankDeposit',
                             back_populates='parent_ba')

    # Polymorphic relationship
    @property
    def entity(self):
        if self.counterparty_type == 'Retail':
            return self.session.query(Retail).filter_by(id=self.counterparty_id).first()
        elif self.counterparty_type == 'Institutional':
            return self.session.query(Institutional).filter_by(id=self.counterparty_id).first()

    def __repr__(self):
        return (f"<BankAccount(id={self.id}, counterparty_id={self.counterparty_id}, "
                f"counterparty_type='{self.counterparty_type}', number={self.number}, "
                f"bank_name='{self.bank_name}', bank_address='{self.bank_address}', "
                f"swift_bic_code='{self.swift_bic_code}', iban='{self.iban}', "
                f"onboarding_timestamp={self.onboarding_timestamp})>")

    def to_dict(self):
        return {
            'id': self.id,
            'counterparty_id': self.counterparty_id,
            'counterparty_type': self.counterparty_type,
            'number': self.number,
            'bank_name': self.bank_name,
            'bank_address': self.bank_address,
            'swift_bic_code': self.swift_bic_code,
            'iban': self.iban,
            'onboarding_timestamp': self.onboarding_timestamp.isoformat() if self.onboarding_timestamp else None
        }

class BankDeposit(Base):
    __tablename__ = 'bank_deposits'
    __table_args__ = {'schema': schema_deposits}
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_account_id = Column(Integer, ForeignKey('funding_sources.bank_accounts.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('account.currencies.id'), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    initiation_timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    confirmation_timestamp = Column(DateTime(timezone=True), nullable=True)
    transaction_number = Column(String(100), nullable=False)
    receipt_id = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)

    parent_ba = relationship('BankAccount', back_populates='child_bd')
    parent_c = relationship('Currencies', back_populates='child_bd')

    def __repr__(self):
        return (f"<BankDeposit(id={self.id}, bank_account_id={self.bank_account_id}, "
                f"currency_id={self.currency_id}, amount={self.amount}, fee={self.fee}, "
                f"initiation_timestamp={self.initiation_timestamp}, confirmation_timestamp={self.confirmation_timestamp}, "
                f"transaction_number='{self.transaction_number}', receipt_id='{self.receipt_id}', "
                f"status='{self.status}')>")

    def to_dict(self):
        return {
            'id': self.id,
            'bank_account_id': self.bank_account_id,
            'currency_id': self.currency_id,
            'amount': self.amount,
            'fee': self.fee,
            'initiation_timestamp': self.initiation_timestamp.isoformat() if self.initiation_timestamp else None,
            'confirmation_timestamp': self.confirmation_timestamp.isoformat() if self.confirmation_timestamp else None,
            'transaction_number': self.transaction_number,
            'receipt_id': self.receipt_id,
            'status': self.status
        }

class CryptoDeposit(Base):
    __tablename__ = 'crypto_deposits'
    __table_args__ = {'schema': schema_deposits}
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey('funding_sources.wallets.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('account.currencies.id'), nullable=False)
    usd_amount = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    initiation_timestamp = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    confirmation_timestamp = Column(DateTime(timezone=True), nullable=True)
    transaction_number = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)

    parent_w = relationship('Wallet', back_populates='child_cd')
    parent_c = relationship('Currencies', back_populates='child_cd')

    def __repr__(self):
        return (f"<CryptoDeposit(id={self.id}, wallet_id={self.wallet_id}, "
                f"currency_id={self.currency_id}, usd_amount={self.usd_amount}, fee={self.fee}, "
                f"initiation_timestamp={self.initiation_timestamp}, confirmation_timestamp={self.confirmation_timestamp}, "
                f"transaction_number='{self.transaction_number}', "
                f"status='{self.status}')>")

    def to_dict(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'currency_id': self.currency_id,
            'usd_amount': self.usd_amount,
            'fee': self.fee,
            'initiation_timestamp': self.initiation_timestamp.isoformat() if self.initiation_timestamp else None,
            'confirmation_timestamp': self.confirmation_timestamp.isoformat() if self.confirmation_timestamp else None,
            'transaction_number': self.transaction_number,
            'status': self.status
        }

class Instrument(Base):
    __tablename__ = 'instruments'
    __table_args__ = {'schema': schema_trades}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Instrument(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
# junction table to associate one portfolio to many trades
trades_to_portfolios = Table(
    'trades_to_portfolios', Base.metadata,
    Column('trade_id', Integer, ForeignKey('trades.trades.id'), primary_key=True),
    Column('portfolio_id', Integer, ForeignKey('trades.portfolios.id'), primary_key=True),
    schema=schema_trades  # Explicitly setting the schema to 'trades'
)

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__ = {'schema': schema_trades}

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50))

    portfolios = relationship(
        'Portfolio',
        secondary=trades_to_portfolios,
        back_populates='trades'
    )

    def __repr__(self):
        return f"<Trade(id={self.id}, description='{self.description}')>"

class Portfolio(Base):
    __tablename__ = 'portfolios'
    __table_args__ = {'schema': schema_trades}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    trades = relationship(
        'Trade',
        secondary=trades_to_portfolios,
        back_populates='portfolios'
    )

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}')>"

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


# OLD DATABASE

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
