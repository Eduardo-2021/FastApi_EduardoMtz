import models, schemas
from Conexion import SessionLocal,engine
from typing import List
from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get('/usuarios/', response_model=List[schemas.User])
def show_users(db:Session=Depends(get_db)):
    usuarios = db.query(models.User).all()
    return usuarios

@app.post('/usuarios/', response_model=schemas.User)
def create_users(entrada:schemas.User,db:Session=Depends(get_db)):
    usuario = models.User(username=entrada.username,nombre=entrada.nombre,rol=entrada.rol,estado=entrada.estado)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put('/usuarios/{usuario_id}', response_model=schemas.User)
def update_users(usuario_id:int,entrada:schemas.UserUpdate,db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    usuario.nombre = entrada.nombre
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete('/usuarios/{usuario_id}', response_model=schemas.Respuesta)
def delete_users(usuario_id:int,db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(Mensaje="Eliminado con éxito")
    return respuesta

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
