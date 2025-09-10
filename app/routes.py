from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database


router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/todos", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_todo

@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}