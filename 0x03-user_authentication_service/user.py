#!/usr/bin/env python3
"""
Defines the User model for a SQLAlchemy database table named users.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for the model
Base = declarative_base()

class User(Base):
    """
    User SQLAlchemy model for the users table.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
