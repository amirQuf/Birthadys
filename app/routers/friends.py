from fastapi import HTTPException, status, Depends, APIRouter
import crud, schemas
from dependencies import get_db
from sqlalchemy.orm import Session
from datetime import date


friends_router = APIRouter()


@friends_router.get("/friend/")
async def retrieve_all_Friends(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of friends with optional pagination.

    Parameters:
    - skip (int): Number of records to skip (default: 0).
    - limit (int): Maximum number of records to retrieve (default: 100).
    - db (Session): SQLAlchemy database session.

    Returns:
    - List[schemas.Friend]: List of friend records.
    """
    friends = crud.get_friends(db, skip=skip, limit=limit)
    return friends


@friends_router.get("/today-birthdays")
async def retrieve_birthday_buddies(db: Session = Depends(get_db)):
    """
    Retrieve friends with birthdays matching the current date.

    Parameters:
    - db (Session): SQLAlchemy database session.

    Returns:
    - Union[List[schemas.Friend], dict]: List of friends or a message indicating no birthdays.
    """
    today = date.today()
    friends = crud.get_birthdays_buddy(db=db, today=today)
    if not friends:
        return {"message": "no birthday buddies for today.", "result": []}
    return friends


@friends_router.get("/friend/{id}", response_model=schemas.Friend)
async def retrieve_birthdate(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a friend by their ID.

    Parameters:
    - id (int): ID of the friend to retrieve.
    - db (Session): SQLAlchemy database session.

    Returns:
    - schemas.Friend: The friend record.

    Raises:
    - HTTPException(404): If the friend does not exist.
    """
    friend = crud.get_friend(id=id, db=db)
    if friend:
        return friend
    raise HTTPException(
        detail="friend doesn't exist", status_code=status.HTTP_404_NOT_FOUND
    )


@friends_router.post("/friend/add", response_model=schemas.Friend)
async def add_friend(
    friend: schemas.FriendIn, db: Session = Depends(get_db)
) -> schemas.Friend:
    """
    Add a new friend to the database.

    Parameters:
    - friend (schemas.FriendIn): Friend information to be added.
    - db (Session): SQLAlchemy database session.

    Returns:
    - schemas.Friend: The newly added friend.

    Raises:
    - HTTPException(400): If an error occurs during the addition process.
    """
    try:
        new_friend = crud.add_friend(friend=friend, db=db)
        return new_friend
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
