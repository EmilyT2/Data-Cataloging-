from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

# 1. Initialize the API
app = FastAPI(title="Pharma Data Catalog API")

# Allow the React frontend to communicate with this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Mocking the merged DataFrames (Normally loaded from your CSVs or Database)
# Here we simulate the final, cleaned data after applying the pandas logic discussed earlier.
master_index_data = [
    {
        "id": "entity_1",
        "matchTerms": ['semaglutide', 'ozempic', 'wegovy', 'rybelsus', 'nvo', 'novo nordisk'],
        "data": {
            "generic": "Semaglutide",
            "brands": "Ozempic, Wegovy, Rybelsus",
            "manufacturer": "Novo Nordisk",
            "indications": "Type 2 Diabetes, Weight Management",
            "ticker": "NVO",
            "stockPrice": "124.50 USD",
            "trials": 14,
            "phase": "Phase 3",
            "reports": "4,500",
            "seriousRate": "4.2%"
        }
    },
    {
        "id": "entity_2",
        "matchTerms": ['tirzepatide', 'mounjaro', 'zepbound', 'lly', 'eli lilly'],
        "data": {
            "generic": "Tirzepatide",
            "brands": "Mounjaro, Zepbound",
            "manufacturer": "Eli Lilly",
            "indications": "Type 2 Diabetes, Weight Management",
            "ticker": "LLY",
            "stockPrice": "752.10 USD",
            "trials": 8,
            "phase": "Phase 3",
            "reports": "2,100",
            "seriousRate": "3.8%"
        }
    }
]

# 3. Create the Search Endpoint
@app.get("/api/search")
def search_catalog(query: str):
    """
    This endpoint takes a search query from the React frontend,
    scans the master index, and returns the unified data object.
    """
    clean_query = query.lower().strip()
    
    # Search logic: Look through the master index for a matching term
    for entity in master_index_data:
        # Check if the clean_query exactly matches or is contained within the mapped terms
        if any(clean_query == term or clean_query in term for term in entity["matchTerms"]):
            return {"status": "success", "result": entity["data"]}
            
    # If no match is found, return a 404 error
    raise HTTPException(status_code=404, detail="No results found in the current catalog index.")

# 4. Status Endpoint (Just to check if the server is running)
@app.get("/")
def read_root():
    return {"message": "Data Catalog API is running. Send queries to /api/search?query=YOUR_TERM"}

# --- Instructions to Run ---
# If you save this file as main.py, you run the server using this command in your terminal:
# uvicorn main:app --reload