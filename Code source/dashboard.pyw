# dashboard.pyw (PARTIE 1)
import os
import json
import hashlib
from datetime import datetime
import customtkinter as ctk
from config import DOSSIER_CIBLE, FICHIER_CONFIG_JSON, FICHIER_JSON

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panneau d'Administration et Supervision Sécurisé")
        self.geometry("850x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        os.makedirs(DOSSIER_CIBLE, exist_ok=True)
        self.config_data = self.charger_config()
        self.logs_charges = []

        if "admin_password_hash" not in self.config_data:
            self.ecran_initialisation_password()
        else:
            self.ecran_connexion()

    def charger_config(self):
        if os.path.exists(FICHIER_CONFIG_JSON):
            try:
                with open(FICHIER_CONFIG_JSON, "r", encoding="utf-8") as f: return json.load(f)
            except Exception: pass
        return {}

    def hacher_password(self, password): 
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def ecran_initialisation_password(self):
        self.nettoyer_fenetre()
        ctk.CTkLabel(self, text="Définir le mot de passe Administrateur", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=30)
        self.entry_new_pwd = ctk.CTkEntry(self, placeholder_text="Mot de passe fort", show="*", width=250)
        self.entry_new_pwd.pack(pady=15)
        ctk.CTkButton(self, text="Créer le mot de passe", command=self.enregistrer_premier_password).pack(pady=20)

    def enregistrer_premier_password(self):
        pwd = self.entry_new_pwd.get()
        if len(pwd) < 4: return
        self.config_data["admin_password_hash"] = self.hacher_password(pwd)
        self.config_data.update({"intervalle_perf": 10, "intervalle_apps": 5, "degre_surveillance": "Standard", "taille_max_logs_mo": 10})
        self.sauvegarder_fichier_config()
        self.construire_interface_principale()

    def ecran_connexion(self):
        self.nettoyer_fenetre()
        ctk.CTkLabel(self, text="Accès Protégé - Saisir le mot de passe", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=40)
        self.entry_login_pwd = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*", width=250)
        self.entry_login_pwd.pack(pady=10)
        self.lbl_erreur = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_erreur.pack(pady=5)
        ctk.CTkButton(self, text="Se connecter", command=self.verifier_connexion).pack(pady=20)

    def verifier_connexion(self):
        if self.hacher_password(self.entry_login_pwd.get()) == self.config_data.get("admin_password_hash"): 
            self.construire_interface_principale()
        else:
            self.lbl_erreur.configure(text="Mot de passe incorrect.")

    def construire_interface_principale(self):
        self.nettoyer_fenetre()
        self.tabview = ctk.CTkTabview(self, width=820, height=560)
        self.tabview.pack(padx=15, pady=15)
        
        self.tab_config = self.tabview.add("⚙️ Réglages Moteur")
        self.tab_logs = self.tabview.add("📊 Visionneuse de Logs JSON")
        
        self.generer_onglet_config()
        self.generer_onglet_logs()

    def generer_onglet_config(self):
        ctk.CTkLabel(self.tab_config, text="Configuration Globale du Système", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        ctk.CTkLabel(self.tab_config, text="Degré de surveillance :").pack(pady=2)
        self.combo_degre = ctk.CTkComboBox(self.tab_config, values=["Léger", "Standard", "Global"])
        self.combo_degre.set(self.config_data.get("degre_surveillance", "Standard"))
        self.combo_degre.pack(pady=5)

        ctk.CTkLabel(self.tab_config, text="Fréquence de capture Performance (secondes) :").pack(pady=2)
        self.slider_perf = ctk.CTkSlider(self.tab_config, from_=5, to=60, number_of_steps=11)
        self.slider_perf.set(self.config_data.get("intervalle_perf", 10))
        self.slider_perf.pack(pady=5)

        ctk.CTkLabel(self.tab_config, text="Taille max des logs avant compression (Mo) :").pack(pady=2)
        self.slider_taille = ctk.CTkSlider(self.tab_config, from_=5, to=100, number_of_steps=19)
        self.slider_taille.set(self.config_data.get("taille_max_logs_mo", 10))
        self.slider_taille.pack(pady=5)

        from config import DOSSIER_LOGS
        btn_logs = ctk.CTkButton(self.tab_config, text="📁 Ouvrir l'explorateur de fichiers Logs", command=self.ouvrir_dossier_logs, fg_color="#107c41", hover_color="#0b592e")
        btn_logs.pack(pady=15)

        btn_save = ctk.CTkButton(self.tab_config, text="Enregistrer et Quitter", command=self.appliquer_modifications, fg_color="#2b82c9")
        btn_save.pack(pady=15)

# dashboard.pyw (PARTIE 2)
    def generer_onglet_logs(self):
        frame_filtres = ctk.CTkFrame(self.tab_logs, height=50)
        frame_filtres.pack(fill="x", padx=5, pady=5)

        self.filtre_cat = ctk.CTkOptionMenu(frame_filtres, values=["TOUT", "PERF", "APPLICATIONS"], width=120, command=self.filtrer_et_afficher_logs)
        self.filtre_cat.pack(side="left", padx=10, pady=10)

        self.recherche_entry = ctk.CTkEntry(frame_filtres, placeholder_text="Rechercher un mot-clé (ex: chrome)...", width=300)
        self.recherche_entry.pack(side="left", padx=10, pady=10)
        self.recherche_entry.bind("<KeyRelease>", self.filtrer_et_afficher_logs)

        btn_refresh = ctk.CTkButton(frame_filtres, text="🔄 Actualiser", width=100, command=self.charger_logs_depuis_json)
        btn_refresh.pack(side="right", padx=10, pady=10)

        self.zone_tableau = ctk.CTkScrollableFrame(self.tab_logs, width=780, height=400)
        self.zone_tableau.pack(fill="both", expand=True, padx=5, pady=5)

        self.charger_logs_depuis_json()

    def charger_logs_depuis_json(self):
        self.logs_charges = []
        if os.path.exists(FICHIER_JSON):
            try:
                with open(FICHIER_JSON, "r", encoding="utf-8") as f:
                    for ligne in f:
                        if ligne.strip(): self.logs_charges.append(json.loads(ligne))
            except Exception: pass
        self.logs_charges.reverse()
        self.filtrer_et_afficher_logs()

    def filtrer_et_afficher_logs(self, event=None):
        for widget in self.zone_tableau.winfo_children(): widget.destroy()

        categorie_cible = self.filtre_cat.get()
        mot_cle = self.recherche_entry.get().lower()

        header_font = ctk.CTkFont(weight="bold", size=13)
        ctk.CTkLabel(self.zone_tableau, text="Horodatage", font=header_font, width=150, anchor="w", text_color="#2b82c9").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.zone_tableau, text="Type", font=header_font, width=100, anchor="w", text_color="#2b82c9").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.zone_tableau, text="Description de l'Événement", font=header_font, width=480, anchor="w", text_color="#2b82c9").grid(row=0, column=2, padx=10, pady=5, sticky="w")

        ligne_index = 1
        for log in self.logs_charges:
            type_log = log.get("type", "")
            timestamp = log.get("timestamp", "")
            description = log.get("data", {}).get("description", "")

            if categorie_cible != "TOUT" and type_log != categorie_cible: continue
            if mot_cle and mot_cle not in description.lower() and mot_cle not in type_log.lower(): continue

            bg_text_color = "#ffffff" if ligne_index % 2 == 0 else "#aaaaaa"
            
            ctk.CTkLabel(self.zone_tableau, text=timestamp, width=150, anchor="w", text_color=bg_text_color).grid(row=ligne_index, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.zone_tableau, text=type_log, width=100, anchor="w", text_color="#2b82c9" if type_log == "PERF" else "#e67e22").grid(row=ligne_index, column=1, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.zone_tableau, text=description, width=480, anchor="w", text_color=bg_text_color).grid(row=ligne_index, column=2, padx=10, pady=2, sticky="w")

            ligne_index += 1

        if ligne_index == 1:
            ctk.CTkLabel(self.zone_tableau, text="Aucun log ne correspond aux critères de recherche.", text_color="gray").grid(row=1, column=0, columnspan=3, pady=20)

    def ouvrir_dossier_logs(self):
        from config import DOSSIER_LOGS
        if os.path.exists(DOSSIER_LOGS): os.startfile(DOSSIER_LOGS)

    def appliquer_modifications(self):
        self.config_data.update({
            "degre_surveillance": self.combo_degre.get(), "intervalle_perf": int(self.slider_perf.get()),
            "intervalle_apps": 5 if self.combo_degre.get() != "Léger" else 15, "taille_max_logs_mo": int(self.slider_taille.get())
        })
        self.sauvegarder_fichier_config()
        self.destroy()

    def sauvegarder_fichier_config(self):
        with open(FICHIER_CONFIG_JSON, "w", encoding="utf-8") as f: json.dump(self.config_data, f, indent=4)

    def nettoyer_fenetre(self):
        for widget in self.winfo_children(): widget.destroy()

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
