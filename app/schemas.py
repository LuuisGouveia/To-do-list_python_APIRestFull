from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True




class TodoBase(BaseModel):
    title: str
    description: str | None = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: bool    
    

class Todo(TodoBase):
    id: int
    completed: bool
    
    class Config:
        orm_mode = True