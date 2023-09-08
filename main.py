from fastapi import FastAPI ,HTTPException , status ,Depends
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from  datetime  import date

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



def get_db():
    db =SessionLocal()
    try:
        yield db 
    finally:
        db.close()





@app.get('/friend/' ,response_model=schemas.Friend , status_code=200)
async def retrieve_all_Friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    friends = crud.get_friends(db, skip=skip, limit=limit)
    return friends

@app.get('/today/' ,response_model=schemas.Friend , status_code=200)
async def retrieve_birthday_buddies(db: Session = Depends(get_db)):
    today = date.today()
    friends = crud.get_birthdays_buddy(db=db , today=today)
    if not friends:
        return {"message":"no birthday buddies for today.", "result":[]} 
    return friends



@app.get('/friend/{id}' , response_model=schemas.Friend,status_code=200)
async def retrieve_birthdate(id :int, db: Session = Depends(get_db)):
    friend = crud.get_friend(id=id, db=db)
    if friend :
        return friend
    raise HTTPException(detail="friend doesn't exist", status_code=status.HTTP_404_NOT_FOUND)


@app.post('/friend/add',response_model=schemas.Friend)
async def add_friend(friend:schemas.FriendIn, db: Session = Depends(get_db) )-> schemas.Friend:
    try:
        new_friend = crud.add_friend(friend=friend, db=db)
        return new_friend
    except:
        raise HTTPException(detail="something is wrong", status_code=status.HTTP_400_BAD_REQUEST)







if __name__ =="__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)