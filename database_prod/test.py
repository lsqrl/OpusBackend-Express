from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# Create a base class
Base = declarative_base()

url = URL.create(
    drivername="postgresql",
    username="cece",
    password="holland2023",
    host="localhost",
    port=5432,
    database="uzh"#"postgres"
)
# Define a table in schema 'schema1'
class UserSchema1(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'schema1'}  # Specify the schema here

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Define a table in schema 'schema2'
class UserSchema2(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'schema2'}  # Specify the schema here

    id = Column(Integer, primary_key=True)
    email = Column(String)

# Define the engine (replace with your actual database URL)
engine = create_engine(url)

connection = engine.connect()

Base.metadata.drop_all(engine)
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS schema1"))
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS schema2"))
    connection.commit()
# Create all tables in the Base metadata across different schemas
Base.metadata.create_all(engine)

# Optionally, create a session to interact with the tables
Session = sessionmaker(bind=engine)
session = Session()

# Example: Adding records to tables in different schemas
user1 = UserSchema1(name='John Doe')
user2 = UserSchema2(email='johndoe@example.com')

session.add(user1)
session.add(user2)
session.commit()

# Always remember to close the session
session.close()
