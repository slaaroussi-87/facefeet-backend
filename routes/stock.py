from fastapi import APIRouter
from supabase import Client
from datetime import datetime

router = APIRouter()

def get_router(supabase: Client):

    @router.get("/")
    def get_stock():
        try:
            res = supabase.table("produits").select("id, nom, stock, seuil_alerte, categories(nom)").order("nom").execute()
        except Exception:
            res = supabase.table("produits").select("id, nom, stock, categories(nom)").order("nom").execute()
            for p in res.data:
                p.setdefault("seuil_alerte", 5)
        return res.data or []

    @router.get("/alertes")
    def get_alertes():
        try:
            res = supabase.table("produits").select("id, nom, stock, seuil_alerte, categories(nom)").order("nom").execute()
        except Exception:
            res = supabase.table("produits").select("id, nom, stock, categories(nom)").order("nom").execute()
            for p in res.data:
                p.setdefault("seuil_alerte", 5)
        produits = res.data or []
        return [p for p in produits if (p.get("stock") or 0) <= (p.get("seuil_alerte") or 5)]

    @router.get("/mouvements")
    def get_mouvements():
        res = (
            supabase.table("mouvements_stock")
            .select("*, produits(nom)")
            .order("date", desc=True)
            .order("heure", desc=True)
            .limit(50)
            .execute()
        )
        return res.data

    @router.put("/{produit_id}")
    def update_stock(produit_id: str, data: dict):
        payload = {"stock": data["stock"]}
        if "seuil_alerte" in data and data["seuil_alerte"] is not None:
            payload["seuil_alerte"] = data["seuil_alerte"]
        res = supabase.table("produits").update(payload).eq("id", produit_id).execute()
        return res.data

    @router.post("/mouvement")
    def create_mouvement(data: dict):
        now = datetime.now()

        prod = supabase.table("produits").select("stock").eq("id", data["produit_id"]).execute()
        current_stock = prod.data[0].get("stock") or 0
        if data["type"] == "entree":
            new_stock = current_stock + data["quantite"]
        else:
            new_stock = max(0, current_stock - data["quantite"])

        supabase.table("produits").update({"stock": new_stock}).eq("id", data["produit_id"]).execute()

        # Historique optionnel — ignoré si la table n'existe pas encore
        try:
            mouvement = {
                "produit_id": data["produit_id"],
                "type": data["type"],
                "quantite": data["quantite"],
                "motif": data.get("motif", ""),
                "date": now.strftime("%Y-%m-%d"),
                "heure": now.strftime("%H:%M:%S"),
            }
            supabase.table("mouvements_stock").insert(mouvement).execute()
        except Exception:
            pass

        return {"message": "Mouvement enregistré", "nouveau_stock": new_stock}

    return router
