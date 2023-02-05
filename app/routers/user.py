from typing import List
# from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException, Response, status
from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity
import datetime
import json

from app.database import User
from .. import schemas, oauth2

router = APIRouter()

# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

@router.get('/all')
def get_all(user_id: str = Depends(oauth2.require_admin)):
    users = []
    for u in User.find():
    #   x = userResponseEntity(u)
      users.append(userResponseEntity(u))
    # print(users)
    resp = {"status": "success", "users": json.dumps(users, cls=DateTimeEncoder)}
    print(resp)
    # return resp
    return {"status": "success", "users": users}
    # return {"status": "success", "users": json.dumps(users, cls=DateTimeEncoder)}


@router.delete('/delete/{email}')
def delete_user(email: str, user_id: str = Depends(oauth2.require_admin)):
    user = User.find_one_and_delete({'email': email.lower()})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with email {email} not found')
    # post = Post.find_one_and_delete({'_id': ObjectId(id)})
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'No post with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/me', response_model=schemas.UserResponse)
def get_me(user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}
