from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import os

import shutil

from convert_json import ConvertToJson

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def upload_excel(file: UploadFile = File(...)):
    # Guardar el archivo temporalmente
    temp_file_path = f"./file/temp.xlsx"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        

    converter = ConvertToJson()
    
    # Pasar el archivo a la función convert_json.main()
    result = converter.convert(file_path=temp_file_path)
    
    # Eliminar el archivo temporal
    os.remove(temp_file_path)
    
    # Devolver el resultado JSON
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)