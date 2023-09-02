from fastapi import FastAPI ,HTTPException , status
from datetime import date
from typing import List
from pydantic import BaseModel



app = FastAPI()

birthdays = []

#models
class Birthdate(BaseModel):
    date : date
    name: str


#routers
@app.get('/birth/')
async def retrieve_all_birthdays()->List[Birthdate]:
    return birthdays

@app.get('/birth/{id}')
async def retrieve_birthdate(id :int)->Birthdate:
    if birthdays[id]:
        return birthdays[id]
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@app.post('/birth/')
async def create_birthday(birthdate:Birthdate)->dict:
    birthdays.append(birthdate)
    return {"message":"birthdate added"}



@app.delete('/birth/{id}')
async def delete_birthday(id:int)->dict:
    if birthdays[id]:
        birthdays.remove(id)
        return {"message":"birthdate deleted!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


if __name__ =="__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)