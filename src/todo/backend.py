from sqlalchemy.orm import Session,DeclarativeBase,Mapped,mapped_column
from sqlalchemy import create_engine,ForeignKey,select
from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    pass

class viewStructure(BaseModel):
    id: int
    task: str
    status: bool

class completedStructure(BaseModel):
    id: int
    task: int

dbUrl=getenv("dbUrl")
try:
    engine=create_engine(dbUrl)
except:
    raise KeyError("No Db Connection Url Provided")

class Tasks(Base):
    __tablename__='tasks'
    id:Mapped[int]=mapped_column(primary_key=True)
    task:Mapped[str]=mapped_column(nullable=False)
    status:Mapped[str]=mapped_column(nullable=False)

class CompletedTasks(Base):
    __tablename__="completedtasks"
    id:Mapped[int]=mapped_column(primary_key=True)
    task:Mapped[str]=mapped_column(nullable=False)

Base.metadata.create_all(engine)


def addTask(task,status):
    taskObj=Tasks(task=task,status=status)
    if taskObj:
        with Session(engine) as session:
            session.add(taskObj)
            session.commit()

def markCompleted(task):
    taskObj=CompletedTasks(task=task)
    if taskObj:
        with Session(engine) as session:
            session.add(taskObj)
            session.commit()

def loadTasks(table):
    if table.lower().strip()=='completed':
        obj=CompletedTasks
    elif table.lower().strip()=='alltasks':
        obj=Tasks
    with Session(engine) as session:
        query=select(obj)
        return session.scalars(query).all()

def delTask(table,title):
    tbClass=Tasks if table.lower().strip()=='alltasks' else CompletedTasks

    with Session(engine) as session:
        query=select(tbClass).where(tbClass.task==title)
        task=session.scalars(query).first()
        if task:
            session.delete(task)
            session.commit()