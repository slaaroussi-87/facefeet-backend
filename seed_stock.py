import random
import sys
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ── 1. Vérification des colonnes ───────────────────────────────────────────────
print("=== Vérification des colonnes ===")

colonnes_manquantes = []

try:
    supabase.table("produits").select("stock").limit(1).execute()
    print("  [OK] Colonne 'stock' présente")
except Exception:
    colonnes_manquantes.append("stock")
    print("  [X] Colonne 'stock' manquante")

try:
    supabase.table("produits").select("seuil_alerte").limit(1).execute()
    print("  [OK] Colonne 'seuil_alerte' présente")
except Exception:
    colonnes_manquantes.append("seuil_alerte")
    print("  [X] Colonne 'seuil_alerte' manquante")

if colonnes_manquantes:
    print("\n/!\\  Colonnes manquantes :", ", ".join(colonnes_manquantes))
    print("   Exécute ce SQL dans Supabase > SQL Editor :\n")
    print("   ALTER TABLE produits ADD COLUMN IF NOT EXISTS stock integer DEFAULT 0;")
    print("   ALTER TABLE produits ADD COLUMN IF NOT EXISTS seuil_alerte integer DEFAULT 5;")
    print()
    sys.exit(1)

# ── 2. Vérification de la table mouvements_stock ──────────────────────────────
print("\n=== Vérification de la table mouvements_stock ===")
try:
    supabase.table("mouvements_stock").select("id").limit(1).execute()
    print("  [OK] Table 'mouvements_stock' presente")
except Exception:
    print("  [!] Table 'mouvements_stock' absente - a creer dans Supabase pour l'historique")
    print("      (le peuplement du stock continue quand meme)\n")

# ── 3. Mise à jour des produits ───────────────────────────────────────────────
print("\n=== Mise à jour des stocks ===")

produits = supabase.table("produits").select("id, nom").execute().data
print(f"  {len(produits)} produits trouvés\n")

for p in produits:
    stock_val = random.randint(10, 100)
    supabase.table("produits").update({
        "stock": stock_val,
        "seuil_alerte": 5
    }).eq("id", p["id"]).execute()
    barre = "#" * (stock_val // 10) + "." * (10 - stock_val // 10)
    print(f"  [OK] {p['nom']:<25} stock: {stock_val:>3}  [{barre}]  seuil: 5")

print(f"\n*** {len(produits)} produits mis à jour avec succès !")
print("   Relance uvicorn et rafraîchis la page Stock.")
