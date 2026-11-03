# config.py
import os

DOSSIER_CIBLE = r"C:\ProgramData\AdvancedSystemTelemetry"
DOSSIER_LOGS = os.path.join(DOSSIER_CIBLE, "Logs")

FICHIER_CONFIG_JSON = os.path.join(DOSSIER_CIBLE, "config.json")
FICHIER_INTERNE_ERREURS = os.path.join(DOSSIER_LOGS, "app_internal_errors.log")
FICHIER_TXT = os.path.join(DOSSIER_LOGS, "user_readable_activity.log")
FICHIER_JSON = os.path.join(DOSSIER_LOGS, "machine_readable_activity.json")

NOM_APPLICATION = "AdvancedSystemTelemetry"
