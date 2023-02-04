from lib.database import DBConnection as DB
from datetime import datetime


class GenshinPhoto:
    def __init__(self, user_id: int, url: str, date: datetime):
        self.user_id = user_id
        self.url = url
        self.date = date


def add_photo_list(genshin_photos: list[GenshinPhoto]):
    with DB(auto_commit=True) as db:
        db.insert(
            table="genshin_photo",
            columns="user_id, url",
            values=[(photo.user_id, photo.url) for photo in genshin_photos],
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


def get_photo_url_list() -> list[str]:
    with DB(auto_commit=False) as db:
        result = db.select(
            sql="""
            select url
            from genshin_photo
            """,
        )
        return [v[0] for v in result]


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
                    url varchar(512) not null unique
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
