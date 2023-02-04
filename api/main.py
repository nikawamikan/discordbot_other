from fastapi import FastAPI
from model.genshin_photo import get_photo_url_list
app = FastAPI()


@app.get("/")
async def genshin_photo():
    return {"urls": get_photo_url_list()}
