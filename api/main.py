import uvicorn
from fastapi import FastAPI

from api.authentication.auth_router import router as auth_roter
from api.routes.router import main_router

app = FastAPI()

app.include_router(main_router)
app.include_router(auth_roter)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
