from fastapi import FastAPI, Depends

from . import config

from .routers import docs
from .routers import groups


app = FastAPI()

app.include_router(docs.router)
app.include_router(groups.router)



@app.get("/info")
async def get_info(settings = Depends(config.get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.database_string,
    }





