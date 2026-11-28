from sqlalchemy.orm import Session,DeclarativeBase,Mapped,mapped_column,relationship,joinedload
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
    taskId: int

dbUrl=getenv("dbUrl")
try:
    engine=create_engine(dbUrl)
except:
    raise KeyError("No Db Connection Url Provided")

class Tasks(Base):
    __tablename__='tasks'
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(nullable=False)
    status:Mapped[str]=mapped_column(nullable=False)
    completedTask=relationship('CompletedTasks',back_populates='task',
                               cascade='all,delete-orphan',
                               uselist=False)

class CompletedTasks(Base):
    __tablename__="completedtasks"
    id:Mapped[int]=mapped_column(primary_key=True)
    taskId:Mapped[int]=mapped_column(ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False,unique=True)
    task=relationship('Tasks',back_populates="completedTask")

Base.metadata.create_all(engine)


def addTask(task,status):
    taskObj=Tasks(title=task,status=status)
    if taskObj:
        with Session(engine) as session:
            session.add(taskObj)
            session.commit()

def markCompleted(title):
    with Session(engine) as session:
        query=select(Tasks).where(Tasks.title==title)
        taskObj=session.scalars(query).first()
        taskObj.status='completed'
        session.add(CompletedTasks(taskId=taskObj.id))
        session.commit()

def loadAllTasks():
    with Session(engine) as session:
        query=select(Tasks)
        return session.scalars(query).all()

def loadCompletedTasks():
    with Session(engine) as session:
        query=select(CompletedTasks).options(joinedload(CompletedTasks.task))
        return session.scalars(query).all()

def delTask(title):

    with Session(engine) as session:
        query=select(Tasks).where(Tasks.title==title)
        task=session.scalars(query).first()
        if task:
            session.delete(task)
            session.commit()

def undoTask(title):
    with Session(engine) as session:
        query=select(Tasks).where(Tasks.title==title)
        task=session.scalars(query).first()
        if task:
            task.status='incomplete'
            completedTask=task.completedTask
            session.delete(completedTask)
            session.commit()