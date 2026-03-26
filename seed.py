from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# 1. Créer les catégories
categories = ["Bijoux", "Jeux", "Maroquinerie", "Deco", "Cosmetiques", "Chaussures", "Textile"]

# Supprimer l'ancienne catégorie "Chaussures" pour éviter les doublons
supabase.table("categories").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

print("Insertion des catégories...")
cat_map = {}
for cat in categories:
    res = supabase.table("categories").insert({"nom": cat}).execute()
    cat_map[cat] = res.data[0]["id"]
    print(f"  ✓ {cat}")

# 2. Créer les produits
produits = [
    {"nom": "Brac M", "categorie": "Bijoux", "prix_achat": 20, "prix_vente": 150, "reference": "REF-001"},
    {"nom": "Brac Art", "categorie": "Bijoux", "prix_achat": 10, "prix_vente": 50, "reference": "REF-002"},
    {"nom": "Collier M", "categorie": "Bijoux", "prix_achat": 20, "prix_vente": 200, "reference": "REF-003"},
    {"nom": "Bague", "categorie": "Bijoux", "prix_achat": 20, "prix_vente": 150, "reference": "REF-004"},
    {"nom": "BO", "categorie": "Bijoux", "prix_achat": 5, "prix_vente": 100, "reference": "REF-005"},
    {"nom": "Jeu de cartes", "categorie": "Jeux", "prix_achat": 30, "prix_vente": 150, "reference": "REF-006"},
    {"nom": "Trousse", "categorie": "Maroquinerie", "prix_achat": 5, "prix_vente": 15, "reference": "REF-007"},
    {"nom": "Magnet", "categorie": "Deco", "prix_achat": 8, "prix_vente": 30, "reference": "REF-008"},
    {"nom": "Sac chabka G", "categorie": "Maroquinerie", "prix_achat": 60, "prix_vente": 200, "reference": "REF-009"},
    {"nom": "Sac crochet", "categorie": "Maroquinerie", "prix_achat": 70, "prix_vente": 300, "reference": "REF-010"},
    {"nom": "Huile argan L", "categorie": "Cosmetiques", "prix_achat": 60, "prix_vente": 300, "reference": "REF-011"},
    {"nom": "Creme fdb L", "categorie": "Cosmetiques", "prix_achat": 65, "prix_vente": 250, "reference": "REF-012"},
    {"nom": "Serum fdb L", "categorie": "Cosmetiques", "prix_achat": 60, "prix_vente": 200, "reference": "REF-013"},
    {"nom": "Brume sdm", "categorie": "Cosmetiques", "prix_achat": 90, "prix_vente": 250, "reference": "REF-014"},
    {"nom": "Ceinture M", "categorie": "Maroquinerie", "prix_achat": 25, "prix_vente": 200, "reference": "REF-015"},
    {"nom": "Ceinture cuir", "categorie": "Maroquinerie", "prix_achat": 60, "prix_vente": 300, "reference": "REF-016"},
    {"nom": "Bougie nhas", "categorie": "Deco", "prix_achat": 38, "prix_vente": 200, "reference": "REF-017"},
    {"nom": "Mules raphia", "categorie": "Chaussures", "prix_achat": 60, "prix_vente": 300, "reference": "REF-018"},
    {"nom": "Porte cles", "categorie": "Deco", "prix_achat": 6, "prix_vente": 50, "reference": "REF-019"},
    {"nom": "Babouches perles", "categorie": "Chaussures", "prix_achat": 150, "prix_vente": 500, "reference": "REF-020"},
    {"nom": "Masque G", "categorie": "Cosmetiques", "prix_achat": 200, "prix_vente": 1000, "reference": "REF-021"},
    {"nom": "Masque P", "categorie": "Cosmetiques", "prix_achat": 100, "prix_vente": 300, "reference": "REF-022"},
    {"nom": "Echarpe", "categorie": "Textile", "prix_achat": 30, "prix_vente": 200, "reference": "REF-023"},
]

print("\nInsertion des produits...")
for p in produits:
    data = {
        "nom": p["nom"],
        "categorie_id": cat_map[p["categorie"]],
        "prix_achat": p["prix_achat"],
        "prix_vente": p["prix_vente"],
        "reference": p["reference"],
        "stock": 0,
        "actif": True
    }
    supabase.table("produits").insert(data).execute()
    print(f"  ✓ {p['nom']} ({p['categorie']}) - {p['prix_vente']} DH")

print("\n🎉 Base de données alimentée avec succès !")
print(f"   {len(categories)} catégories")
print(f"   {len(produits)} produits")