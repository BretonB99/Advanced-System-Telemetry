# main.pyw
import time
import asyncio
import logging
import config
from security import appliquer_securite_ntfs, inscrire_au_demarrage
from writer import DoubleFormatWriter
from capteurs.performance import CapteurPerformance
from capteurs.applications import CapteurApplications

logging.basicConfig(filename=config.FICHIER_INTERNE_ERREURS, level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

async def execution_principale():
    appliquer_securite_ntfs()
    inscrire_au_demarrage()
    writer = DoubleFormatWriter()
    capteur_perf = CapteurPerformance(writer)
    capteur_apps = CapteurApplications(writer)
    taches = [asyncio.create_task(capteur_perf.surveiller()), asyncio.create_task(capteur_apps.surveiller())]
    await asyncio.gather(*taches)

if __name__ == "__main__":
    while True:
        try: asyncio.run(execution_principale())
        except Exception as c:
            logging.critical(f"CRASH : {str(c)}. Relancement dans 10s...")
            time.sleep(10)
