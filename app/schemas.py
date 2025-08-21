from pydantic import BaseModel, EmailStr, ConfigDict, conint
from pydantic.types import conint
from datetime import datetime
from typing import Literal, Optional

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class CreatePost(PostBase):
  pass

class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)

class ResponsePost(PostBase):
  id: int
  created_by: UserOut
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
  Post: ResponsePost
  votes: int

  model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[int] = None

class Vote(BaseModel):
  post_id: int
  dir: Literal[0,1]