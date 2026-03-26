from fastapi import APIRouter
from supabase import Client

router = APIRouter()

def get_router(supabase: Client):

    @router.get("/")
    def get_produits():
        res = supabase.table("produits").select("*, categories(nom)").execute()
        return res.data

    @router.post("/")
    def create_produit(data: dict):
        res = supabase.table("produits").insert(data).execute()
        return res.data

    @router.put("/{id}")
    def update_produit(id: str, data: dict):
        res = supabase.table("produits").update(data).eq("id", id).execute()
        return res.data

    @router.delete("/{id}")
    def delete_produit(id: str):
        res = supabase.table("produits").delete().eq("id", id).execute()
        return {"message": "Produit supprimé"}

    return router