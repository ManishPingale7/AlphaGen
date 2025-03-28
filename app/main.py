from fastapi import FastAPI
from app.edu.router import router as edu_rouster  
from app.creative.router import router as creative_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AlphaGen")


origins =[
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(edu_router)
app.include_router(creative_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AlphaGen!"}



