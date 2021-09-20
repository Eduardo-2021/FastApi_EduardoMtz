from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
datos = {"1": "Python", "2": "Java", "3": "Php", "4": "JavaScript", "5": "C++"}

@app.get("/")
def raiz(request:Request):
    sin_codificar = json.dumps(datos)
    json_datos = json.loads(sin_codificar)
    return templates.TemplateResponse("inicio.html",{"request":request, "listado":json_datos})

@app.post("/agregar")
async def agregar(request:Request):
    nuevos_datos= {}
    form_data = await request.form()
    i = 1
    for id in datos:
        nuevos_datos[str(id)] = datos[id]
        i+=1
    datos[str(i)] = form_data["nuevolenguaje"]
    sin_codificar = json.dumps(datos)
    json.loads(sin_codificar)
    return RedirectResponse("/",303)

@app.get("/eliminar/{id}")
async def eliminar(requet:Request,id:str):
    del datos[id]
    return RedirectResponse("/",303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")