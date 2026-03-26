from fastapi import APIRouter
from supabase import Client

router = APIRouter()

def get_router(supabase: Client):

    @router.get("/")
    def get_categories():
        res = supabase.table("categories").select("*").execute()
        return res.data

    @router.post("/")
    def create_categorie(data: dict):
        res = supabase.table("categories").insert(data).execute()
        return res.data

    @router.put("/{id}")
    def update_categorie(id: str, data: dict):
        res = supabase.table("categories").update(data).eq("id", id).execute()
        return res.data

    @router.delete("/{id}")
    def delete_categorie(id: str):
        res = supabase.table("categories").delete().eq("id", id).execute()
        return {"message": "Catégorie supprimée"}

    return router