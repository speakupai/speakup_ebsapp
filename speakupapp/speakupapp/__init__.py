from typing import Mapping
from fastapi import FastAPI

def create_app():
    app=FastAPI()

    with app.add_route():
        from . import main
        return app