from fastapi import APIRouter, Depends, status, Response
from .. import schemas, database, models
from sqlalchemy.orm import session
from .. repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# creating user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: session = Depends(get_db)):
    return user.create(request, db)

# get user
@router.get('/{id}', status_code=status.HTTP_200_OK)
def showuser(id, response: Response, db: session = Depends(get_db)):
    return user.show(id, db)
