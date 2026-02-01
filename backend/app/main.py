from fastapi import FastAPI

from app.api.upload_routes import router


app = FastAPI(title="IDAP")
app.include_router(router)
