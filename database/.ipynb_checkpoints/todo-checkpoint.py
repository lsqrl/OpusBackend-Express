# Immutable tables vs access rights for users
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
