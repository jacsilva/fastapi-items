from fastapi import FastAPI, Depends

from . import config

from .routers import items
from .routers import groups


app = FastAPI()

app.include_router(items.router)
app.include_router(groups.router)

my_items = [
    {'id': 1, 'title': 'django, o filme', 'content': 'conteúdo django', 'published': True, 'rating': 2},
    {'id': 2, 'title': 'fast, a api', 'content': 'conteúdo fast', 'published': False, 'rating': 3}
]


@app.get("/info")
async def get_info(settings = Depends(config.get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.database_string,
    }


# request method GET latest item
# @app.get("/items/latest")
# def get_latest_item():
#     item = my_items[len(my_items)-1]
#     return {"detail": item}




