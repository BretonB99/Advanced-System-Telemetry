# security.py
import os
import sys
import winreg
import logging
import win32security
import ntsecuritycon as con
from config import DOSSIER_CIBLE, DOSSIER_LOGS, NOM_APPLICATION

def appliquer_securite_ntfs():
    for chemin in [DOSSIER_CIBLE, DOSSIER_LOGS]:
        try:
            if not os.path.exists(chemin): os.makedirs(chemin, exist_ok=True)
            sd = win32security.GetFileSecurity(chemin, win32security.DACL_SECURITY_INFORMATION)
            dacl = win32security.ACL()
            sid_system = win32security.ConvertStringSidToSid("S-1-5-18")
            sid_admins = win32security.ConvertStringSidToSid("S-1-5-32-544")
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, sid_system)
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, sid_admins)
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            sd.SetSecurityDescriptorControl(win32security.SE_DACL_PROTECTED, win32security.SE_DACL_PROTECTED)
            win32security.SetFileSecurity(chemin, win32security.DACL_SECURITY_INFORMATION, sd)
        except Exception as e: logging.error(f"Erreur NTFS : {str(e)}")

def inscrire_au_demarrage():
    chemin_script = os.path.abspath(sys.argv)
    commande = f'"{os.path.join(os.path.dirname(sys.executable), "pythonw.exe")}" "{chemin_script}"' if chemin_script.endswith(('.py', '.pyw')) else f'"{chemin_script}"'
    try:
        cle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(cle, NOM_APPLICATION, 0, winreg.REG_SZ, commande)
        winreg.CloseKey(cle)
    except Exception as e: logging.error(f"Erreur Registre : {str(e)}")
