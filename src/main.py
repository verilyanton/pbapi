from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router.health import HealthRouter
from src.router.search import SearchRouter

app = FastAPI(title='Vegan API')
app.include_router(HealthRouter)
app.include_router(SearchRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
