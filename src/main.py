import os
import sys
import uvicorn
from queries.orm import SyncORM
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from routers import hero
print("DB_HOST:", os.getenv("DB_HOST"))
def main():
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    SyncORM.create_tables()
    SyncORM.insert_heroes()
    SyncORM.get_heroes_with_abbilities()
def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"],
    )
    app.include_router(hero.router)
    
    return app
app = create_fastapi_app()
if __name__ == "__main__":
    main()
    if "--webserver" in sys.argv:
        uvicorn.run(
            app="src.main:app",
            reload=True,
        )