from pydantic import BaseModel
from datetime import date


class Birthdate(BaseModel):
    name: str
    birthday : date| None = None
    mobile:str| None = None
    email:str | None = None

