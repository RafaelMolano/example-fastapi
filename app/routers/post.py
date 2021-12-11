from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import Base, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
#def get_posts():
    #sql_select_Query = 'Select * From products'
    #my_posts = newConection.fetch(sql_select_Query, params=None) 
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    
   
    my_posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

 
    return my_posts   

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(new_post: Post):
#     sql_select_Query = '''Insert into products (title, content, published) values (%s, %s, %s)'''
#     my_new_posts = newConection.fetchone(sql_select_Query, params=(new_post.title, new_post.content, new_post.published)) 
#     return {"data": my_new_posts}  
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Esta opción no es funcional por tener que escribir todos los atributos
    #my_new_posts = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)

    #Por eso es mejor a través de diccionarios (** extrae toda la estructura)
    print(current_user.email)
    my_new_posts = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(my_new_posts)
    db.commit()
    db.refresh(my_new_posts)
    return my_new_posts

@router.get("/{id}", response_model=schemas.PostOut)
# def get_post(id: int):
#     sql_select_Query = 'Select * From products Where Id = %s'
#     id_str = str(id) 
#     my_posts = newConection.fetch(sql_select_Query, params=(id_str,)) 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #my_posts = db.query(models.Post).filter(models.Post.id == id).first()
    my_posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message:" f"post with id: {id} was not found"}

    return my_posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     sql_select_Query = 'Delete From products Where Id = %s'
#     id_str = str(id) 
#     deleted_posts = newConection.fetch(sql_select_Query, params=(id_str,)) 
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_posts = posts_query.first()

    if deleted_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    #Controlar que no puede actualizar/borrar posts de otros usuarios
    if deleted_posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    posts_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
# def update_post(id: int, post: Post):
#     sql_select_Query = 'Update products Set Title = %s,content = %s, published = %s Where Id = %s'
#     id_str = str(id) 
#     updated_posts = newConection.fetch(sql_select_Query, params=(post.title, post.content, post.published,)) 
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts_query = db.query(models.Post).filter(models.Post.id == id)
    updated_posts = posts_query.first()

    if updated_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    #Controlar que no puede actualizar/borrar posts de otros usuarios
    if updated_posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    posts_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return posts_query.first()