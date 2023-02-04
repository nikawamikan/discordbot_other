from datetime import datetime
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI
from model.genshin_photo import get_photo_url_list, get_photo_path_list
app = FastAPI()
CURRENT = Path() / "images"


@app.get("/api")
async def genshin_photo(limit: int = None, max_width: int = None, shuffle: bool = True):
    return {"urls": get_photo_url_list(limit=limit, max_width=max_width, shuffle=shuffle)}


@app.get("/api/photo/list")
async def get_photo_url_list(limit: int = None, size: str = "fullhd", shuffle: bool = True):
    return {"urls": get_photo_path_list(limit=limit, size=size, shuffle=shuffle)}


@app.get("/api/photo/{size:path}/{filename:path}")
async def get_file(size: str, filename: str):
    """画像ファイルを取得します

    Args:
        size (str): thumbnail, fullhd, original のいずれかの文字列
        filename (str): ファイルの名称(短縮名)

    Returns:
        FileResponse: 画像データ
    """

    file_path = CURRENT / size / filename
    now = datetime.now()

    response = FileResponse(
        path=file_path,
        filename=f"{filename}"
    )

    return response
