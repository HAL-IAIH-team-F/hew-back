from hew_back import app


@app.get("/api")
async def health():
    return {"ok": True}
