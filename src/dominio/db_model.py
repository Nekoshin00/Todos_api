from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

class StatusModel(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    tasks = relationship('TaskModel', back_populates='status')

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)

    folders = relationship('FolderModel', back_populates='user', cascade='all, delete-orphan')

class FolderModel(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=True)

    user = relationship('UserModel', back_populates='folders')
    tasks = relationship('TaskModel', back_populates='folder', cascade='all, delete-orphan')

class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    folder_id = Column(Integer, ForeignKey('folders.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False, default=1)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    folder = relationship('FolderModel', back_populates='tasks')
    status = relationship('StatusModel', back_populates='tasks')
 
