# writer.py
import os
import json
import gzip
import shutil
import logging
import threading
from datetime import datetime
from config import FICHIER_TXT, FICHIER_JSON, FICHIER_CONFIG_JSON

class DoubleFormatWriter:
    def __init__(self):
        self.chemin_txt = FICHIER_TXT
        self.chemin_json = FICHIER_JSON

    def extraire_taille_max(self):
        if os.path.exists(FICHIER_CONFIG_JSON):
            try:
                with open(FICHIER_CONFIG_JSON, "r", encoding="utf-8") as f: return int(json.load(f).get("taille_max_logs_mo", 10)) * 1024 * 1024
            except Exception: pass
        return 10 * 1024 * 1024

    def verifier_et_compresser(self, chemin):
        taille_max_octets = self.extraire_taille_max()
        if os.path.exists(chemin) and os.path.getsize(chemin) > taille_max_octets:
            try:
                horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_archive = chemin + f"_{horodatage}.bak"
                os.rename(chemin, nom_archive)
                threading.Thread(target=self._compresser_worker, args=(nom_archive,), daemon=True).start()
            except Exception as e: logging.error(f"Échec rotation : {str(e)}")

    def _compresser_worker(self, chemin_bak):
        try:
            with open(chemin_bak, 'rb') as f_in, gzip.open(chemin_bak + ".gz", 'wb', compresslevel=6) as f_out: shutil.copyfileobj(f_in, f_out)
            os.remove(chemin_bak)
        except Exception as e: logging.error(f"Échec compression : {str(e)}")

    def enregistrer_evenement(self, categorie, message_dict):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.verifier_et_compresser(self.chemin_txt)
        try:
            with open(self.chemin_txt, "a", encoding="utf-8") as f: f.write(f"[{horodatage}] [{categorie.upper()}] {message_dict.get('description', '')}\n")
        except Exception: pass
        self.verifier_et_compresser(self.chemin_json)
        try:
            with open(self.chemin_json, "a", encoding="utf-8") as f: f.write(json.dumps({"timestamp": horodatage, "type": categorie.upper(), "data": message_dict}) + "\n")
        except Exception: pass
