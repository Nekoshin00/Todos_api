from fastapi import FastAPI, UploadFile
from routes.auth_route import authRouter
from routes.status_route import statusRouter
from routes.folder_route import folderRouter
from routes.task_route import taskRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import aiofiles
from config import PUBLIC_DIR
from connection.connection import create_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(authRouter, tags=["Autenticación"])
app.include_router(statusRouter, prefix="/statuses", tags=["Estados"])
app.include_router(folderRouter, prefix="/folders", tags=["Carpetas"])
app.include_router(taskRouter, prefix="/folders", tags=["Tareas"])

app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get('/')
async def read_root():
    return {"message": "Bienvenido a la ruta raíz de la API."}

'''Solo para pruebas'''
@app.post("/uploadfile/", tags=["Pruebas"], name="Prueba de subida de archivos")
async def upload_file(file: UploadFile):
    path = PUBLIC_DIR / file.filename
    async with aiofiles.open(path, 'wb+') as f:
        content = await file.read() 
        await f.write(content)
    return {"filename": file.filename}

'''Solo util para pruebas'''
@app.get('/create-db', tags=["Pruebas"], name="Crear base de datos")
async def create_database():
    try:
        await create_db()
        return {"message": "Base de datos creada exitosamente."}
    except Exception as e:
        return {"error": str(e)}