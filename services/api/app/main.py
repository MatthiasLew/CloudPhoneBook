from fastapi import FastAPI
from app.api.router import router as api_router

app = FastAPI(title="CloudPhoneBook API")

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "CloudPhoneBook API is running"}
