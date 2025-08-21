from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

app = FastAPI() #instance

# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
   return {"message": "Welcome to my API"}







# def post_by_id(id):
#    for p in my_posts:
#       if p['id'] == id:
#          return p
      
# def post_index(id):
#    for i, c in enumerate(my_posts):
#       if c['id'] == id:
#          return i

# my_posts = [{'title': 'title of post', 'content': 'content of post', 'id': 1},{"title": "Favourite food", "content": "I like paneer", "id":2}]
