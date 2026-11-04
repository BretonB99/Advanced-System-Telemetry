# capteurs/applications.py
import asyncio
import json
import os
import logging
import psutil
from config import FICHIER_CONFIG_JSON

class CapteurApplications:
    """Surveille les lancements de logiciels selon le profil de l'utilisateur actif."""
    def __init__(self, writer):
        self.writer = writer
        self.processus_connus = set()

    async def surveiller(self):
        # Initialisation : cartographie des processus existants pour éviter les doublons
        try:
            self.processus_connus = {p.pid for p in psutil.process_iter()}
        except Exception:
            pass

        while True:
            # 1. Détecter l'utilisateur actuellement connecté
            sessions = psutil.users()
            nom_utilisateur = sessions[0].name if sessions else "Par_Defaut"

            # Valeurs d'usine par défaut
            actif = True
            intervalle = 5

            # 2. Lecture des règles spécifiques au profil saisies au clavier
            if os.path.exists(FICHIER_CONFIG_JSON):
                try:
                    with open(FICHIER_CONFIG_JSON, "r", encoding="utf-8") as f:
                        config_globale = json.load(f).get("surveillance_utilisateurs", {})
                        
                        cfg_profil = config_globale.get(nom_utilisateur, config_globale.get("Par_Defaut", {}))
                        cfg_capteur = cfg_profil.get("APPLICATIONS", {"actif": True, "intervalle": 5})
                        
                        actif = cfg_capteur.get("actif", True)
                        intervalle = cfg_capteur.get("intervalle", 5)
                except Exception:
                    pass

            # 3. Analyse des lancements uniquement si actif pour cet utilisateur
            if actif:
                try:
                    pids_actuels = set()
                    for p in psutil.process_iter(['pid', 'name', 'username']):
                        try:
                            pid = p.info['pid']
                            pids_actuels.add(pid)
                            
                            # Si un nouveau PID apparaît, on l'enregistre avec le tag utilisateur
                            if pid not in self.processus_connus:
                                donnees = {
                                    "description": f"Lancement de l'application : {p.info['name']} (PID: {pid})",
                                    "user": nom_utilisateur,  # Injection essentielle pour le filtre croisé
                                    "process_name": p.info['name'],
                                    "pid": pid
                                }
                                self.writer.enregistrer_evenement("APPLICATIONS", donnees)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    self.processus_connus = pids_actuels
                except Exception as e:
                    logging.error(f"Erreur CapteurApplications : {str(e)}")
            
            await asyncio.sleep(intervalle)
