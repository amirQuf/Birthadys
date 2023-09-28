from fastapi import HTTPException , status ,Depends , APIRouter
import crud, schemas
from dependencies import get_db
from sqlalchemy.orm import Session
from  datetime  import date


friends_router = APIRouter()

@friends_router.get('/friend/')
async def retrieve_all_Friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''retrieve all the friends '''
    friends = crud.get_friends(db, skip=skip, limit=limit)
    return friends

@friends_router.get('/today-birthdays' )
async def retrieve_birthday_buddies(db: Session = Depends(get_db)):
    '''retrieve all the birthday buddies for today'''
    today = date.today()
    friends = crud.get_birthdays_buddy(db=db , today=today)
    if not friends:
        return {"message":"no birthday buddies for today.", "result":[]} 
    return friends



@friends_router.get('/friend/{id}' , response_model=schemas.Friend)
async def retrieve_birthdate(id :int, db: Session = Depends(get_db)):
    '''retrieve a single friend by id'''
    friend = crud.get_friend(id=id, db=db)
    if friend :
        return friend
    raise HTTPException(detail="friend doesn't exist", status_code=status.HTTP_404_NOT_FOUND)


@friends_router.post('/friend/add',response_model=schemas.Friend)
async def add_friend(friend:schemas.FriendIn, db: Session = Depends(get_db) )-> schemas.Friend:
    '''add a new friend to the database'''
    try:
        new_friend = crud.add_friend(friend=friend, db=db)
        return new_friend
    except:
        raise HTTPException(detail="something is wrong", status_code=status.HTTP_400_BAD_REQUEST)
