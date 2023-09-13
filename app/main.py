from fastapi import FastAPI
from database import engine
from . import models
from routers.friends import friends_router

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(friends_router)


if __name__ =="__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)