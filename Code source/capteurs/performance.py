# capteurs/performance.py
import asyncio
import json
import os
import logging
import psutil
from config import FICHIER_CONFIG_JSON

class CapteurPerformance:
    def __init__(self, writer): self.writer = writer
    async def surveiller(self):
        while True:
            intervalle = 10
            if os.path.exists(FICHIER_CONFIG_JSON):
                try:
                    with open(FICHIER_CONFIG_JSON, "r") as f: intervalle = json.load(f).get("intervalle_perf", 10)
                except Exception: pass
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                self.writer.enregistrer_evenement("PERF", {"description": f"Performances système - CPU: {cpu}% | RAM: {ram}%", "cpu_usage_percent": cpu, "ram_usage_percent": ram})
            except Exception as e: logging.error(f"Erreur Perf : {str(e)}")
            await asyncio.sleep(intervalle)
