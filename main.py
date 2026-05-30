from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()


class ClientData(BaseModel):
    prenom: str
    nom: str
    age: int
    profession: str
    statut_professionnel: str


def generer_numero_dossier():

    compteur_fichier = "compteur.txt"

    if not os.path.exists(compteur_fichier):
        with open(compteur_fichier, "w") as f:
            f.write("1")

    with open(compteur_fichier, "r") as f:
        compteur = int(f.read())

    annee = datetime.now().year

    numero_dossier = f"JCAN-VV-{annee}-{compteur:04d}"

    with open(compteur_fichier, "w") as f:
        f.write(str(compteur + 1))

    return numero_dossier


@app.get("/")
def home():
    return {
        "message": "Visa Backend fonctionne"
    }


@app.post("/analyse-dossier")
def analyse_dossier(client: ClientData):

    if not os.path.exists("dossiers"):
        os.makedirs("dossiers")

    numero_dossier = generer_numero_dossier()

    dossier = {
        "numero_dossier": numero_dossier,
        "prenom": client.prenom,
        "nom": client.nom,
        "age": client.age,
        "profession": client.profession,
        "statut_professionnel": client.statut_professionnel,
        "type_demande": "VV",
        "statut": "Analyse préliminaire",
        "date_creation": datetime.now().strftime("%Y-%m-%d")
    }

    nom_fichier = (
        f"dossiers/{numero_dossier} "
        f"({client.prenom} {client.nom}).json"
    )

    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(dossier, f, ensure_ascii=False, indent=4)

    return {
        "message": "Dossier enregistré avec succès",
        "numero_dossier": numero_dossier,
        "fichier": nom_fichier,
        "statut": "Analyse préliminaire"
    }