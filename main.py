from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
from database import get_db

# Initialize App as 'app'
app = FastAPI()

# Creating a path object for the templates folder
templates_folder = Path(__file__).parent / "templates"

# Creating a path object for the static folder within the templates folder
static_folder = templates_folder / "static"

# Static and templates initialization
app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(templates_folder)

# list of accepted origins
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.get("/")


def home(request: Request, db: Session = Depends(get_db)):
    ...
