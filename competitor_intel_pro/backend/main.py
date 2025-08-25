from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud import get_all_competitors

app = FastAPI(title="Competitor Intelligence API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only; change for production
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/competitors")
def read_competitors():
    """
    Returns a list of all competitors in JSON format.
    """
    return get_all_competitors()
