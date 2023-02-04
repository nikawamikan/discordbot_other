from lib.database import DBConnection as DB
from datetime import datetime
import os

HOST_URL = os.getenv("HOST_URL")


class GenshinPhoto:
    def __init__(self, user_id: int, width: int, height: int,  message_id: int, url: str, date: datetime, filename: str):
        self.user_id = user_id
        self.url = url
        self.date = date
        self.message_id = message_id
        self.width = width
        self.height = height
        self.filename = filename


def add_photo_list(genshin_photos: list[GenshinPhoto]):
    with DB(auto_commit=True) as db:
        db.insert(
            table="genshin_photo",
            columns="user_id, message_id, width, height, url, filename",
            values=[(photo.user_id, photo.message_id, photo.width, photo.height,  photo.url, photo.filename)
                    for photo in genshin_photos],
            ignore=True,
        )
        db.execute(
            sql="""
            update date_memo
            set date=%s
            where type='last_genshin_photo_date'
            """,
            values=(max([photo.date for photo in genshin_photos]),),
        )


def delete_photo(message_id):
    with DB(auto_commit=True) as db:
        db.execute(
            sql="""
            delete from genshin_photo
            where message_id = %s
            """,
            values=((message_id,),),
        )


def get_photo_path_list(limit: int, size: str, shuffle: bool) -> list[str]:
    with DB(auto_commit=False) as db:
        limstr = ""
        shufstr = ""
        if limit is not None:
            if 1 > limit:
                raise ValueError(
                    "The minimum value of limit must be at least 1."
                )
            limstr = f"limit {limit}"
            max_widthstr = ", width, height"
        if shuffle:
            shufstr = "order by rand()"
        sql = f"""
            select filename
            from genshin_photo
            {shufstr}
            {limstr}
            """
        result = db.select(
            sql=sql,
        )
        urls = [
            f"{HOST_URL}/api/photo/{size}/{v[0]}" for v in result]
        return urls


def get_photo_url_list(limit: int, max_width: int, shuffle: bool) -> list[str]:
    with DB(auto_commit=False) as db:
        limstr = ""
        max_widthstr = ""
        shufstr = ""
        if limit is not None:
            if 1 > limit:
                raise ValueError(
                    "The minimum value of limit must be at least 1."
                )
            limstr = f"limit {limit}"
        if max_width is not None:
            if 100 > max_width > 2000:
                raise ValueError(
                    "max_width ranges from 100 to 2000."
                )
            max_widthstr = ", width, height"
        if shuffle:
            shufstr = "order by rand()"

        sql = f"""
            select url{max_widthstr}
            from genshin_photo
            {shufstr}
            {limstr}
            """
        print(sql)
        result = db.select(
            sql=sql,
        )
        if max_width is None:
            urls = [v[0] for v in result]
        else:
            urls = [
                f"{v[0]}?width={max_width}&height={v[2]*max_width//v[1]}"
                for v in result
            ]
        return urls


def get_last_date() -> datetime:
    with DB(auto_commit=False) as db:
        result = db.select(
            sql="""
            select date from date_memo
            where type='last_genshin_photo_date'
            """,
        )
        return result[0][0]


def init_table():
    try:
        with DB(auto_commit=True) as db:
            db.execute(
                sql="""
                create table date_memo(
                    date datetime not null,
                    type varchar(128) not null primary key
                )
                """
            )
            db.execute(
                sql="""
                create table genshin_photo(
                    id int not null auto_increment primary key,
                    user_id bigint not null,
                    message_id bigint not null,
                    width int not null,
                    height int not null,
                    url varchar(512) not null unique,
                    filename varchar(64) not null
                )
                """
            )
            db.insert(
                table="date_memo",
                columns="date, type",
                values=((datetime.min, "last_genshin_photo_date"),)
            )

    except:
        print("table exsit")
