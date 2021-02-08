#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26
"""

# 1. Library imports
from starlette.responses import FileResponse
import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os
from pathlib import Path
from inference import inference
from utils.spectrogram import create_spectrogram

UPLOAD_FOLDER = 'uploads'

# 2. Create app and model objects
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

#3. Welcome page
@app.get("/", response_class=HTMLResponse)
async def read_root(request:Request):
    return templates.TemplateResponse("welcome.html", {"request": request, "message":"message"})

@app.post("/uploads")
async def create_upload_file(request:Request,
                            response: FileResponse,
                            #background_tasks:BackgroundTasks,
                            file: UploadFile = File(...), 
                            ):
    
    tmp_uploads_path = './uploads/'

    if not os.path.exists(tmp_uploads_path):
        os.makedirs(tmp_uploads_path)

    p = Path(tmp_uploads_path + file.filename)
    p_new = Path(tmp_uploads_path+file.filename[:-4]+'_denoised.wav')
    save_uploaded_file(file, p)

    #background_tasks.add_task(create_spectrogram(p), message='your file is being processed')
    create_spectrogram(p, value='_orig')
    
    #  run inference
    inference(p)
    create_spectrogram(p_new, value='_clean')
    
    #return StreamingResponse(spect, media_type='image/png')
    #return FileResponse(spect)
    return templates.TemplateResponse("upload_page.html", 
                                    {"request": request,
                                    "file_path": p,
                                    "filename": file.filename,
                                    "type":file.content_type})


def save_uploaded_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

@app.post("/spect")
async def spect(request: Request,
                file_path: str, 
                response: StreamingResponse):
    spect_temp = create_spectrogram(file_path)

    spect = open(spect_temp, mode='rb')

    return StreamingResponse(spect, media_type='image/png')

'''@app.get("/inf")
async def run_inference(path):
    inference(path)'''
