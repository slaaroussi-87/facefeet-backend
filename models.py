from pydantic import BaseModel, field_validator
from typing import Optional, List


class CategorieCreate(BaseModel):
    nom: str


class CategorieUpdate(BaseModel):
    nom: str


class ProduitCreate(BaseModel):
    nom: str
    categorie_id: str
    prix_achat: float
    prix_vente: float
    reference: Optional[str] = ""
    stock: Optional[int] = 0
    actif: Optional[bool] = True

    @field_validator("prix_achat", "prix_vente")
    @classmethod
    def prix_positif(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        return v


class ProduitUpdate(BaseModel):
    nom: Optional[str] = None
    categorie_id: Optional[str] = None
    prix_achat: Optional[float] = None
    prix_vente: Optional[float] = None
    reference: Optional[str] = None
    stock: Optional[int] = None
    actif: Optional[bool] = None


class LigneVenteCreate(BaseModel):
    produit_id: str
    quantite: int
    prix_unitaire: float

    @field_validator("quantite")
    @classmethod
    def quantite_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La quantité doit être au moins 1")
        return v


class VenteCreate(BaseModel):
    date_vente: Optional[str] = None
    remise_pourcent: Optional[float] = 0
    total: Optional[float] = 0
    lignes: List[LigneVenteCreate]

    @field_validator("remise_pourcent")
    @classmethod
    def remise_valide(cls, v: float) -> float:
        if v is not None and not (0 <= v <= 100):
            raise ValueError("La remise doit être comprise entre 0 et 100")
        return v or 0


class StockUpdate(BaseModel):
    stock: int
    seuil_alerte: Optional[int] = None

    @field_validator("stock")
    @classmethod
    def stock_positif(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        return v


class MouvementCreate(BaseModel):
    produit_id: str
    type: str
    quantite: int
    motif: Optional[str] = ""

    @field_validator("type")
    @classmethod
    def type_valide(cls, v: str) -> str:
        if v not in ("entree", "sortie"):
            raise ValueError("Le type doit être 'entree' ou 'sortie'")
        return v

    @field_validator("quantite")
    @classmethod
    def quantite_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La quantité doit être au moins 1")
        return v
