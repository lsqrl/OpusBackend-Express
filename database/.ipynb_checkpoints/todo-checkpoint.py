# Set the foreign keys and relationship between classes
# Make the classes immutable
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    children = relationship('Child', back_populates='parent')

class Child(Base):
    __tablename__ = 'children'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    
    parent = relationship('Parent', back_populates='children')

# Create an engine and bind the session
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables
Base.metadata.create_all(engine)

# Create a parent object
parent = Parent(name="Parent 1")

# Create child objects and assign them to the parent
child1 = Child(name="Child 1", parent=parent)
child2 = Child(name="Child 2", parent=parent)

# Add the parent (which will also add the children due to the relationship)
session.add(parent)
session.commit()

# Query the parent and access its children
parent = session.query(Parent).filter_by(name="Parent 1").first()
print(f"Parent: {parent.name}")
for child in parent.children:
    print(f"Child: {child.name}")

# Query the child and access its parent
child = session.query(Child).filter_by(name="Child 1").first()
print(f"Child: {child.name}, Parent: {child.parent.name}")





from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ImmutableModel(Base):
    __tablename__ = 'immutable_model'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)
    
    def __setattr__(self, key, value):
        if hasattr(self, key) and key != '_sa_instance_state':
            raise AttributeError(f"Cannot modify attribute '{key}' of immutable instance")
        super().__setattr__(key, value)


from sqlalchemy import event

def make_immutable(mapper, connection, target):
    """Prevent modifications to existing objects"""
    for key in target.__dict__.keys():
        if key != '_sa_instance_state':
            raise AttributeError(f"Cannot modify attribute '{key}' of immutable instance")

event.listen(ImmutableModel, 'before_update', make_immutable)
event.listen(ImmutableModel, 'before_delete', make_immutable)
