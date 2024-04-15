from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.future import select
from databases import Database

DATABASE_URL = "sqlite:///./test_database.db"
database = Database(DATABASE_URL)
Base = declarative_base()


# Define your models
class Workspace(Base):
    __tablename__ = 'workspaces'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    workspace = relationship("Workspace", back_populates="members")


Workspace.members = relationship("Member", order_by=Member.id, back_populates="workspace")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    category = Column(String)
    currency = Column(String)
    date = Column(DateTime)
    name = Column(String)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))


# Set up the database engine and session
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
