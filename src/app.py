from fastapi import FastAPI

app = FastAPI()


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}
