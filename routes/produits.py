from fastapi import APIRouter
from supabase import Client
from models import ProduitCreate, ProduitUpdate

router = APIRouter()

def get_router(supabase: Client):

    @router.get("/")
    def get_produits():
        res = supabase.table("produits").select("*, categories(nom)").execute()
        return res.data

    @router.post("/")
    def create_produit(data: ProduitCreate):
        res = supabase.table("produits").insert(data.model_dump()).execute()
        return res.data

    @router.put("/{id}")
    def update_produit(id: str, data: ProduitUpdate):
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        res = supabase.table("produits").update(payload).eq("id", id).execute()
        return res.data

    @router.delete("/{id}")
    def delete_produit(id: str):
        supabase.table("produits").delete().eq("id", id).execute()
        return {"message": "Produit supprimé"}

    return router
