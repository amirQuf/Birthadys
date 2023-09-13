from pydantic import BaseModel
from datetime import date
from typing import Union

class Friend(BaseModel):
    name: str
    birthday : date 
    mobile:Union[str, None] = None
    email:Union [str , None] = None

class FriendIn(BaseModel):
    name: str
    birthday : Union [date , None] = None
    
