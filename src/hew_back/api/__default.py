from hew_back import app


@app.get("/health")
async def health():
    return {"ok": True}
