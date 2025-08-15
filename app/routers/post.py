from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

# @router.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#    posts = db.query((models.Post))
#    print(posts)
#    return {'data': 'posts'}

#---Path Operations For Posts---

#---GET- ALL POSTS
@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):
  # cursor.execute("""SELECT * FROM posts""")
  # posts = cursor.fetchall()
  #-------------------------------------------------------------------------------
  # print(search.lower())
  posts = db.query(models.Post).filter(func.lower(models.Post.title).contains(search.lower())).limit(limit).offset(skip).all()
  return posts

#---POST- A POST
@router.post('/', status_code = status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.CreatePost, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # post_dict = post.model_dump()
  # post_dict['id'] = randrange(0, 100000000)
  # my_posts.append(post_dict)
  #-------------------------------------------------------------------------------
  # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # conn.commit()
  #-------------------------------------------------------------------------------
  print(current_user.email)
  new_post = models.Post(user_id = current_user.id, **post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

#---GET- POST BY ID
@router.get('/{id}', response_model=schemas.ResponsePost)
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
  # post = cursor.fetchone()
  #-------------------------------------------------------------------------------
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"post with id: {id} not found")
  return post

#---DELETE- A POST BY ID
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  #-------------------------------------------------------------------------------
  deleted_post = db.query(models.Post).filter(models.Post.id == id)
  if deleted_post.first() == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"post with id: {id} Not Found")
  # print(deleted_post, deleted_post.first(), deleted_post.first().user_id)
  if deleted_post.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized")
  deleted_post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code = status.HTTP_204_NO_CONTENT)

#---UPDATE- A POST BY ID
@router.put('/{id}', response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.CreatePost, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
  # updated_post = cursor.fetchone()
  # conn.commit()
  #-------------------------------------------------------------------------------
  post_q = db.query(models.Post).filter(models.Post.id == id)
  post_in_db  = post_q.first()
  if post_in_db == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"post with id: {id} Not Found")
  # print(post_q.first().user_id)
  if post_q.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized")
  post_q.update(post.model_dump(), synchronize_session=False)
  db.commit()
  return post_q.first()
