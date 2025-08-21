from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session 
from app import oauth2, schemas, models
from app.database import get_db



router = APIRouter(
  tags=['Vote']
)

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post_q = db.get(models.Post, vote.post_id)
  if not post_q:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't Exist!")
  vote_q = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
  found_vote = vote_q.first()

  if (vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on {vote.post_id}")
    new_vote = models.Vote(post_id = vote.post_id, user_id =current_user.id)
    db.add(new_vote)
    db.commit()
    return {'message' : 'Successfully added a vote'}
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't Exist!")
    vote_q.delete(synchronize_session=False)
    db.commit()
    return {'message' : 'Successfully deleted a vote'}
