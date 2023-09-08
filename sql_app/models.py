from sqlalchemy import  Column ,Integer, String ,Date
from .database import Base


class Friend(Base):
    __tablename__='Friend'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,unique= True,index=True)
    birthday = Column(Date)
    mobile = Column(String, unique=True)
    email = Column(String, unique=True)

