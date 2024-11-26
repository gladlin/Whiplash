from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    pass
    # return pyatorochka_service.read_root_service()

@app.get("/5ka/")
async def parse_5ka_without_filters(
        query: str
):
    pass
