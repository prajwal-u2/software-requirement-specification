import csv
import os
import re
import json
import urllib.parse
import importlib
import pandas as pd
import subprocess

from urllib.parse import urlencode
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from fastapi.staticfiles import StaticFiles
from core.py.scheduler import Scheduler

app = FastAPI()
environment = "local"
current_dataset = None
authenticated = False

templates = Jinja2Templates(directory="public/template")
app.mount("/asset", StaticFiles(directory="public/asset"), name="asset")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login-page", response_class=HTMLResponse)
async def read_login(request: Request, flash: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "flash": flash})

@app.post("/login", response_class=RedirectResponse)
async def login(email: str = Form(...), password: str = Form(...)):
    if email != "user@example.com" or password != "password":
        extra_params = {
            "flash": "Login successful!",
        }
        redirect_url = f"/login-page?{urlencode(extra_params)}"
        return RedirectResponse(url=redirect_url, status_code=303)
    global authenticated
    authenticated = True
    response = RedirectResponse(url="/schedule-page", status_code=303)
    return response

@app.get("/schedule-page", response_class=HTMLResponse)
async def read_schedule(request: Request):
    # if authenticated:
    return templates.TemplateResponse("schedule.html", {"request": request})
    # else:
    #     return templates.TemplateResponse("login.html", {"request": request, "flash": "login failure"})        

@app.get("/schedule", response_class=JSONResponse)
async def schedule(request: Request, case: str = Query(...)): # case input param
    language = os.getenv("LANGUAGE")
    
    if language == "python":
        exit_code = os.system(f"./bin/py/schedule {case}")
    elif language == "java":
        exit_code = os.system(f"./bin/java/schedule {case}")
    elif language == "cpp":
        exit_code = os.system(f"./bin/cpp/schedule {case}")
    else:
        return JSONResponse({"status": 500, "msg": "Language not supported", "data": json_data})

    path = f"./data/{case}/schedule.csv"
    if not os.path.exists(path):
        return JSONResponse({"status": 500, "msg": f"Error generating schedule for {case}", "data": [], "test_status": "failure", "test_msg": "Error running Scheduler"})

    try:
        df = pd.read_csv(path)
        json_data = df.to_dict(orient="records")
    except:
        return JSONResponse({"status": 500, "msg": f"Error generating schedule for {case}. CSV output file empty.", "data": [], "test_status": "failure", "test_msg": "Empty CSV data"})        
    
    test_status = "Failed"
    test_message = f"Error running {case} test!"
    result = subprocess.run(["./bin/test", f"{case}"], capture_output=True, text=True)
    if result.returncode == 0:
        test_status = "success"
        test_message = f"Test {case} passed!"
    else:
        test_status = "failure"
        test_message = f"Test {case} failed! {result.stderr}"

    if exit_code != 0:
        return JSONResponse({"status": 500, "msg": f"Error generating schedule for {case}", "data": [], "test_status": "failure", "test_msg": "Error running Scheduler"})
    
    return JSONResponse({"status": 200, "msg": f"Schedule successfully retrieved for {case}", "data": json_data, "test_status": test_status, "test_msg": test_message})
