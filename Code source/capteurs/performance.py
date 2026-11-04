# capteurs/performance.py
import asyncio
import json
import os
import logging
import psutil
from config import FICHIER_CONFIG_JSON

class CapteurPerformance:
    """Surveille la charge CPU/RAM selon le profil de l'utilisateur actif."""
    def __init__(self, writer):
        self.writer = writer

    async def surveiller(self):
        while True:
            # 1. Détecter l'utilisateur actuellement connecté à Windows
            sessions = psutil.users()
            nom_utilisateur = sessions[0].name if sessions else "Par_Defaut"

            # Valeurs d'usine par défaut
            actif = True
            intervalle = 10

            # 2. Lecture des règles spécifiques saisies au clavier dans le Dashboard
            if os.path.exists(FICHIER_CONFIG_JSON):
                try:
                    with open(FICHIER_CONFIG_JSON, "r", encoding="utf-8") as f:
                        config_globale = json.load(f).get("surveillance_utilisateurs", {})
                        
                        # Récupère le profil de l'utilisateur ou se rabat sur "Par_Defaut"
                        cfg_profil = config_globale.get(nom_utilisateur, config_globale.get("Par_Defaut", {}))
                        cfg_capteur = cfg_profil.get("PERF", {"actif": True, "intervalle": 10})
                        
                        actif = cfg_capteur.get("actif", True)
                        intervalle = cfg_capteur.get("intervalle", 10)
                except Exception:
                    pass

            # 3. Capture uniquement si l'option est activée pour cet utilisateur précis
            if actif:
                try:
                    cpu = psutil.cpu_percent(interval=None)
                    ram = psutil.virtual_memory().percent
                    
                    donnees = {
                        "description": f"CPU: {cpu}% | RAM: {ram}%",
                        "user": nom_utilisateur,  # Injection essentielle pour le filtre croisé
                        "cpu_usage_percent": cpu,
                        "ram_usage_percent": ram
                    }
                    self.writer.enregistrer_evenement("PERF", donnees)
                except Exception as e:
                    logging.error(f"Erreur CapteurPerformance : {str(e)}")
            
            # Pause asynchrone réglée précisément au clavier
            await asyncio.sleep(intervalle)
