from fastapi import FastAPI

from routes import router
from src.database.utils import create_tables

create_tables()

app = FastAPI()
app.include_router(router)


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}
