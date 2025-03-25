from fastapi import FastAPI
from edu.router import router as edu_router  # Importing the router

app = FastAPI(title="AlphaGen")

app.include_router(edu_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AlphaGen!"}



