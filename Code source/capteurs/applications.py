# capteurs/applications.py
import asyncio
import json
import os
import logging
import psutil
from config import FICHIER_CONFIG_JSON

class CapteurApplications:
    def __init__(self, writer):
        self.writer = writer
        self.processus_connus = set()
    async def surveiller(self):
        try: self.processus_connus = {p.pid for p in psutil.process_iter()}
        except Exception: pass
        while True:
            intervalle = 5
            if os.path.exists(FICHIER_CONFIG_JSON):
                try:
                    with open(FICHIER_CONFIG_JSON, "r") as f: intervalle = json.load(f).get("intervalle_apps", 5)
                except Exception: pass
            try:
                pids_actuels = set()
                for p in psutil.process_iter(['pid', 'name', 'username']):
                    try:
                        pid = p.info['pid']
                        pids_actuels.add(pid)
                        if pid not in self.processus_connus:
                            self.writer.enregistrer_evenement("APPLICATIONS", {"description": f"Application lancée : {p.info['name']} (PID: {pid}) par {p.info['username']}", "process_name": p.info['name'], "pid": pid, "username": p.info['username']})
                    except (psutil.NoSuchProcess, psutil.AccessDenied): continue
                self.processus_connus = pids_actuels
            except Exception as e: logging.error(f"Erreur Apps : {str(e)}")
            await asyncio.sleep(intervalle)
