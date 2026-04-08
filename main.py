from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from supabase import create_client, Client
import os


from routes.categories import get_router as get_categories_router
from routes.produits import get_router as get_produits_router
from routes.ventes import get_router as get_ventes_router
from routes.export import get_router as get_export_router
from routes.stock import get_router as get_stock_router

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="FACE & FEET API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(get_categories_router(supabase), prefix="/categories", tags=["Catégories"])
app.include_router(get_produits_router(supabase), prefix="/produits", tags=["Produits"])
app.include_router(get_ventes_router(supabase), prefix="/ventes", tags=["Ventes"])
app.include_router(get_export_router(supabase), prefix="/export", tags=["Export"])
app.include_router(get_stock_router(supabase), prefix="/stock", tags=["Stock"])

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API FACE & FEET"}

@app.get("/health")
def health():
    try:
        supabase.table("categories").select("id").limit(1).execute()
        return {"status": "ok", "supabase": "connecté"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "supabase": str(e)})