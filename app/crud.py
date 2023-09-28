from sqlalchemy.orm import Session
import models, schemas
from datetime import date
from typing import List
from models import Friend


def get_friend(db: Session, id: int):
    """
    Retrieve a list of friends with optional pagination.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - skip (int): Number of records to skip (default: 0).
    - limit (int): Maximum number of records to retrieve (default: 100).

    Returns:
    - List[models.Friend]: List of friend records.
    """
    return db.query(models.Friend).filter(models.Friend.id == id).first()


def get_birthdays_buddy(db: Session, today: date):
    """
    Retrieve friends with birthdays matching the provided date.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - today (date): Date for birthday comparison.

    Returns:
    - List[models.Friend]: List of friends with matching birthdays.
    """
    result: List[Friend] = []
    friends = db.query(models.Friend).all()
    for friend in friends:
        if friend.birthday.day == today.day and friend.birthday.month == today.month:
            result.append(friend)
    return result


def get_friends(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a friend by their ID.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - id (int): ID of the friend to retrieve.

    Returns:
    - models.Friend: The friend record or None if not found.
    """
    return db.query(models.Friend).offset(skip).limit(limit).all()


def add_friend(db: Session, friend: schemas.Friend):
    """
    Add a new friend to the database.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - friend (schemas.Friend): Friend information to be added.

    Returns:
    - models.Friend: The newly added friend.
    """
    db_friend = models.Friend(**friend.dict())
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend


def search_friends(db: Session, query: str):
    """
    Search for a friend by their name.

    Parameters:
    - db (Session): SQLAlchemy database session.
    - query (str): Name of the friend to search for.

    Returns:
    - models.Friend: The friend record or None if not found.
    """
    return db.query(models.Friend).filter(models.Friend.name.ilike(f"%{query}%")).all()
