from fastapi import APIRouter, HTTPException
from supabase import Client
from datetime import datetime

router = APIRouter()

def get_router(supabase: Client):

    @router.get("/")
    def get_ventes():
        res = supabase.table("ventes").select("*, lignes_vente(*, produits(nom, prix_vente))").execute()
        return res.data

    @router.post("/")
    def create_vente(data: dict):
        lignes = data.get("lignes", [])
        remise_pourcent = data.get("remise_pourcent", 0)

        # ── 1. Validation des stocks avant toute écriture ─────────────────────
        produits_cache = {}
        for ligne in lignes:
            prod = supabase.table("produits").select("id, nom, stock, seuil_alerte").eq("id", ligne["produit_id"]).execute()
            produit = prod.data[0]
            produits_cache[ligne["produit_id"]] = produit
            stock_actuel = produit.get("stock") or 0
            if stock_actuel < ligne["quantite"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuffisant pour '{produit['nom']}' : "
                           f"{stock_actuel} disponible(s), {ligne['quantite']} demandé(s)"
                )

        # ── 2. Création de la vente ────────────────────────────────────────────
        total_brut = sum(l["prix_unitaire"] * l["quantite"] for l in lignes)
        total_remise_val = total_brut * remise_pourcent / 100
        total_net = total_brut - total_remise_val

        now = datetime.now()
        vente = {
            "date": now.strftime("%Y-%m-%d"),
            "heure": now.strftime("%H:%M:%S"),
            "total_brut": total_brut,
            "total_remise": total_remise_val,
            "total_net": total_net
        }
        res = supabase.table("ventes").insert(vente).execute()
        vente_id = res.data[0]["id"]

        # ── 3. Insertion des lignes + décrémentation du stock ─────────────────
        warnings = []
        for ligne in lignes:
            prod_info = supabase.table("produits").select("*").eq("id", ligne["produit_id"]).execute()
            produit = prod_info.data[0]

            prix_vente = ligne["prix_unitaire"]
            quantite = ligne["quantite"]
            prix_achat = produit.get("prix_achat", 0)
            montant_remise = prix_vente * quantite * remise_pourcent / 100
            net = prix_vente * quantite - montant_remise
            marge = net - (prix_achat * quantite)

            ligne_data = {
                "vente_id": vente_id,
                "produit_id": ligne["produit_id"],
                "nom_produit": produit["nom"],
                "reference": produit.get("reference", ""),
                "prix_achat": prix_achat,
                "prix_vente": prix_vente,
                "quantite": quantite,
                "remise": remise_pourcent,
                "type_remise": "pct",
                "montant_remise": montant_remise,
                "net": net,
                "marge": marge
            }
            supabase.table("lignes_vente").insert(ligne_data).execute()

            # Décrémentation du stock
            new_stock = (produit.get("stock") or 0) - quantite
            supabase.table("produits").update({"stock": new_stock}).eq("id", produit["id"]).execute()

            # Warning si sous le seuil après vente
            seuil = produit.get("seuil_alerte") or 5
            if new_stock <= seuil:
                warnings.append({
                    "produit": produit["nom"],
                    "stock_restant": new_stock,
                    "seuil_alerte": seuil
                })

        return {"message": "Vente créée", "vente_id": vente_id, "warnings": warnings}

    @router.delete("/{id}")
    def delete_vente(id: str):
        supabase.table("lignes_vente").delete().eq("vente_id", id).execute()
        supabase.table("ventes").delete().eq("id", id).execute()
        return {"message": "Vente supprimée"}

    @router.delete("/")
    def delete_all_ventes():
        supabase.table("lignes_vente").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("ventes").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        return {"message": "Toutes les ventes supprimées"}

    return router