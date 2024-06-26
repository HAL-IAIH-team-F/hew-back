import uvicorn

from hew_back import app


def main():
    uvicorn.run(app.app, host="0.0.0.0")
