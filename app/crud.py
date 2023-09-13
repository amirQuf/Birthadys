from sqlalchemy .orm import Session
import  models ,schemas
from datetime import date

def get_friend(db:Session,id:int):
    return db.query(models.Friend).filter(models.Friend.id ==id).first()


def get_birthdays_buddy(db:Session , today:date):
    print(today.day)
    print(today.month)
    result =[]
    friends = db.query(models.Friend).all()
    for friend in friends:
        if friend.birthday.day==today.day and friend.birthday.month ==today.month:
            result.append(friend)
    return result




def get_friends(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Friend).offset(skip).limit(limit).all()

def add_friend(db:Session, friend:schemas.Friend):
    db_friend = models.Friend(**friend.dict() )
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend


