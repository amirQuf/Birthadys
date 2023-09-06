from sqlalchemy .orm import Session
from . import  models ,schemas
from datetime import date

def get_friend(db:Session,friend_id:int):
    return db.query(models.Friend).filter(models.Friend.id==friend_id).first()

def get_birthdays_buddy(db:Session , today:date):
    return db.query(models.Friend).filter(models.Friend.birthday==today)


def get_friends(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Friend).offset(skip).limit(limit).all()

def add_friend(db:Session, friend:schemas.Friend):
    db_friend = models.Friend(**friend.dict())
    db.add(db_friend)
    db.commit(db_friend)
    db.refresh(db_friend)
    return db_friend


