import os

import dotenv


class Token:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.refresh_token_expire_minutes = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
        self.access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


class Database:
    def __init__(self):
        self.db_url = os.getenv("DB_URL")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASS")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.validate()

    def validate(self):
        if self.db_url is not None:
            return
        if self.db_user is None:
            raise ValueError("DB_USER must not be None")
        if self.db_pass is None:
            raise ValueError("DB_PASS must not be None")
        if self.db_host is None:
            self.db_host = "localhost"
        if self.db_port is not None:
            self.db_host = f"{self.db_host}:{self.db_port}"
        if self.db_name is None:
            self.db_name = "hew-back"
        if self.db_url is None:
            self.db_url = f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"


class Env:
    def __init__(self):
        dotenv.load_dotenv("./.env.local")
        dotenv.load_dotenv()

        self.cors_list = os.getenv("CORS_LIST")
        self.token = Token()
        self.database = Database()


ENV = Env()
