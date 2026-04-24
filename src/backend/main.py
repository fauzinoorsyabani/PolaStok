from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="PolaStok API",
    description="Backend untuk proyek Capstone PolaStok (Market Insight & Inventory Predition)",
    version="0.1.0"
)

class StatusResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=StatusResponse)
async def root():
    return {
        "status": "success",
        "message": "Backend FastAPI PolaStok berhasil berjalan! AI Module siap diintegrasikan."
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
