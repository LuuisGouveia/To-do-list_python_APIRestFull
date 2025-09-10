from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import database, models, schemas, auth

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_acess_token(token)
    if payload is None:
        raise HTTPException(status_code = 401, detail="Token inválido ou expirado")
    user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login (from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credeciais inválidas")
    token = auth.create_acess_token({'sub': str(user.id)})
    return {'access_token': token, 'token_type': 'bearer'}