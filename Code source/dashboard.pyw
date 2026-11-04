# dashboard.pyw (PARTIE 1)
import os
import json
import hashlib
import customtkinter as ctk
import psutil
from config import DOSSIER_CIBLE, FICHIER_CONFIG_JSON, FICHIER_JSON

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Supervision Système Avancée - Profils et Filtres Multi-Utilisateurs")
        self.geometry("1000x680") # Fenêtre élargie pour un confort visuel optimal
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
        self.config_data.update({
            "taille_max_logs_mo": 10,
            "surveillance_utilisateurs": {
                "Par_Defaut": {
                    "PERF": {"actif": True, "intervalle": 10},
                    "APPLICATIONS": {"actif": True, "intervalle": 5}
                }
            }
        })
        self.sauvegarder_fichier_config()
        self.construire_interface_principale()

    def ecran_connexion(self):
        self.nettoyer_fenetre()
        ctk.CTkLabel(self, text="Saisir le mot de passe Administrateur", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=40)
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

    def lister_utilisateurs_systeme(self):
        """Identifie les comptes Windows réels présents sur le disque dur."""
        utilisateurs = ["Par_Defaut"]
        try:
            dossier_users = r"C:\Users"
            if os.path.exists(dossier_users):
                for nom in os.listdir(dossier_users):
                    chemin = os.path.join(dossier_users, nom)
                    if os.path.isdir(chemin) and nom.lower() not in ["all users", "default", "default user", "public", "desktop.ini"]:
                        utilisateurs.append(nom)
        except Exception: pass
        for u in psutil.users():
            if u.name not in utilisateurs: utilisateurs.append(u.name)
        return utilisateurs

    def construire_interface_principale(self):
        self.nettoyer_fenetre()
        self.tabview = ctk.CTkTabview(self, width=970, height=640)
        self.tabview.pack(padx=10, pady=10)
        
        self.tab_config = self.tabview.add("⚙️ Configuration des Profils")
        self.tab_logs = self.tabview.add("📊 Visionneuse Multi-Critères")
        
        self.generer_onglet_gestion_profils()
        self.generer_onglet_logs()

    def generer_onglet_gestion_profils(self):
        """Interface permettant d'ajouter et configurer un utilisateur indépendamment."""
        frame_ajout = ctk.CTkFrame(self.tab_config)
        frame_ajout.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_ajout, text="Sélectionner un compte local :").pack(side="left", padx=10)
        self.combo_nouvel_user = ctk.CTkOptionMenu(frame_ajout, values=self.lister_utilisateurs_systeme(), width=220)
        self.combo_nouvel_user.pack(side="left", padx=10, pady=10)
        
        btn_add = ctk.CTkButton(frame_ajout, text="➕ Configurer cet utilisateur", command=self.ajouter_utilisateur_profil)
        btn_add.pack(side="left", padx=10, pady=10)

        self.scroll_profils = ctk.CTkScrollableFrame(self.tab_config, width=930, height=400)
        self.scroll_profils.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.redessiner_profils_utilisateurs()

        frame_actions = ctk.CTkFrame(self.tab_config)
        frame_actions.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_actions, text="Taille limite des fichiers logs (Mo) :").pack(side="left", padx=10)
        self.entry_taille_global = ctk.CTkEntry(frame_actions, width=60)
        self.entry_taille_global.insert(0, str(self.config_data.get("taille_max_logs_mo", 10)))
        self.entry_taille_global.pack(side="left", padx=5)

        btn_save = ctk.CTkButton(frame_actions, text="💾 Sauvegarder et Quitter", fg_color="#2b82c9", command=self.sauvegarder_grille_complete)
        btn_save.pack(side="right", padx=10, pady=10)

    def ajouter_utilisateur_profil(self):
        nom = self.combo_nouvel_user.get()
        if nom and nom not in self.config_data.get("surveillance_utilisateurs", {}):
            if "surveillance_utilisateurs" not in self.config_data:
                self.config_data["surveillance_utilisateurs"] = {}
            self.config_data["surveillance_utilisateurs"][nom] = {
                "PERF": {"actif": True, "intervalle": 10},
                "APPLICATIONS": {"actif": True, "intervalle": 5}
            }
            self.redessiner_profils_utilisateurs()

    def redessiner_profils_utilisateurs(self):
        for widget in self.scroll_profils.winfo_children(): widget.destroy()
        self.inputs_dynamiques = {}
        profils = self.config_data.get("surveillance_utilisateurs", {})

        for user, capteurs in profils.items():
            frame_u = ctk.CTkFrame(self.scroll_profils, border_width=1, border_color="#333333")
            frame_u.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(frame_u, text=user, font=ctk.CTkFont(weight="bold", size=14), width=140, anchor="w").pack(side="left", padx=15)

            self.inputs_dynamiques[user] = {}
            for capteur_nom in ["PERF", "APPLICATIONS"]:
                cfg_capteur = capteurs.get(capteur_nom, {"actif": False, "intervalle": 10})
                
                var_check = ctk.BooleanVar(value=cfg_capteur.get("actif", False))
                cb = ctk.CTkCheckBox(frame_u, text=capteur_nom, variable=var_check)
                cb.pack(side="left", padx=10)

                ctk.CTkLabel(frame_u, text="Intervalle (s) :").pack(side="left", padx=2)
                ent = ctk.CTkEntry(frame_u, width=55)
                ent.insert(0, str(cfg_capteur.get("intervalle", 10)))
                ent.pack(side="left", padx=5)

                self.inputs_dynamiques[user][capteur_nom] = {"cb_var": var_check, "entry_int": ent}

            btn_del = ctk.CTkButton(frame_u, text="🗑️", width=40, fg_color="#c0392b", hover_color="#962d22", command=lambda u=user: self.supprimer_profil_user(u))
            btn_del.pack(side="right", padx=15)
# dashboard.pyw (PARTIE 2)
    def supprimer_profil_user(self, nom_user):
        if nom_user in self.config_data["surveillance_utilisateurs"]:
            del self.config_data["surveillance_utilisateurs"][nom_user]
            self.redessiner_profils_utilisateurs()

    def sauvegarder_grille_complete(self):
        nouvelle_carte = {}
        for user, capteurs in self.inputs_dynamiques.items():
            nouvelle_carte[user] = {}
            for capteur_nom, ui_elements in capteurs.items():
                try: val_intervalle = int(ui_elements["entry_int"].get())
                except ValueError: val_intervalle = 10
                
                nouvelle_carte[user][capteur_nom] = {
                    "actif": ui_elements["cb_var"].get(),
                    "intervalle": val_intervalle
                }
        try: taille_log = int(self.entry_taille_global.get())
        except ValueError: taille_log = 10

        self.config_data["taille_max_logs_mo"] = taille_log
        self.config_data["surveillance_utilisateurs"] = nouvelle_carte
        self.sauvegarder_fichier_config()
        self.destroy()

    # --- VISIONNEUSE DE LOGS MULTI-CRITÈRES ---
    def generer_onglet_logs(self):
        """Crée une barre d'outils avec filtres cumulatifs croisés (Type + User + Recherche)."""
        frame_filtres = ctk.CTkFrame(self.tab_logs)
        frame_filtres.pack(fill="x", padx=5, pady=5)

        # Filtre 1 : Le capteur ciblé
        ctk.CTkLabel(frame_filtres, text="Capteur:").pack(side="left", padx=5)
        self.filtre_cat = ctk.CTkOptionMenu(frame_filtres, values=["TOUT", "PERF", "APPLICATIONS"], width=110, command=self.filtrer_et_afficher_logs)
        self.filtre_cat.pack(side="left", padx=5, pady=10)

        # Filtre 2 : L'utilisateur ciblé (Détecté de manière dynamique)
        ctk.CTkLabel(frame_filtres, text="Utilisateur:").pack(side="left", padx=5)
        self.filtre_user = ctk.CTkOptionMenu(frame_filtres, values=["TOUT"], width=130, command=self.filtrer_et_afficher_logs)
        self.filtre_user.pack(side="left", padx=5, pady=10)

        # Filtre 3 : Recherche par mot-clé textuel
        self.recherche_entry = ctk.CTkEntry(frame_filtres, placeholder_text="Rechercher un mot-clé ou un PID...", width=240)
        self.recherche_entry.pack(side="left", padx=10, pady=10)
        self.recherche_entry.bind("<KeyRelease>", self.filtrer_et_afficher_logs)

        # Bouton d'actualisation de la mémoire cache
        btn_refresh = ctk.CTkButton(frame_filtres, text="🔄 Actualiser", width=90, command=self.charger_logs_depuis_json)
        btn_refresh.pack(side="right", padx=10, pady=10)

        # Zone du tableau défilant
        self.zone_tableau = ctk.CTkScrollableFrame(self.tab_logs, width=930, height=450)
        self.zone_tableau.pack(fill="both", expand=True, padx=5, pady=5)
        self.charger_logs_depuis_json()

    def charger_logs_depuis_json(self):
        """Lit l'historique et met à jour dynamiquement la liste des utilisateurs trouvés."""
        self.logs_charges = []
        liste_users_trouves = set()
        
        if os.path.exists(FICHIER_JSON):
            try:
                with open(FICHIER_JSON, "r", encoding="utf-8") as f:
                    for ligne in f:
                        if ligne.strip():
                            bloc_data = json.loads(ligne)
                            self.logs_charges.append(bloc_data)
                            
                            # Extraction de l'utilisateur stocké dans le JSON pour enrichir le filtre
                            u_name = bloc_data.get("data", {}).get("user")
                            if u_name: liste_users_trouves.add(u_name)
            except Exception: pass
            
        self.logs_charges.reverse() # Tri chronologique inversé (Plus récent en premier)
        
        # Mettre à jour le filtre déroulant des utilisateurs avec les vrais noms trouvés dans les rapports
        menu_utilisateurs = ["TOUT"] + sorted(list(liste_users_trouves))
        self.filtre_user.configure(values=menu_utilisateurs)
        
        self.filtrer_et_afficher_logs()

    def filtrer_et_afficher_logs(self, event=None):
        """Applique les 3 filtres cumulatifs en simultané et redessine la grille."""
        for widget in self.zone_tableau.winfo_children(): widget.destroy()

        cat_cible = self.filtre_cat.get()
        user_cible = self.filtre_user.get()
        mot_cle = self.recherche_entry.get().lower()

        # Construction des en-têtes du tableau
        font_h = ctk.CTkFont(weight="bold", size=13)
        ctk.CTkLabel(self.zone_tableau, text="Horodatage", font=font_h, width=140, anchor="w", text_color="#2b82c9").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.zone_tableau, text="Capteur", font=font_h, width=100, anchor="w", text_color="#2b82c9").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.zone_tableau, text="Utilisateur", font=font_h, width=110, anchor="w", text_color="#2b82c9").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.zone_tableau, text="Description de l'événement", font=font_h, width=500, anchor="w", text_color="#2b82c9").grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ligne_idx = 1
        for log in self.logs_charges:
            type_log = log.get("type", "")
            timestamp = log.get("timestamp", "")
            user_log = log.get("data", {}).get("user", "Inconnu")
            description = log.get("data", {}).get("description", "")

            # Validation du Filtre 1 : Capteur
            if cat_cible != "TOUT" and type_log != cat_cible: continue
            # Validation du Filtre 2 : Utilisateur
            if user_cible != "TOUT" and user_log != user_cible: continue
            # Validation du Filtre 3 : Mot-clé textuel
            if mot_cle and (mot_cle not in description.lower() and mot_cle not in type_log.lower() and mot_cle not in user_log.lower()): continue

            # Rendu visuel alterné
            couleur_ligne = "#ffffff" if ligne_idx % 2 == 0 else "#aaaaaa"
            
            ctk.CTkLabel(self.zone_tableau, text=timestamp, width=140, anchor="w", text_color=couleur_ligne).grid(row=ligne_idx, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.zone_tableau, text=type_log, width=100, anchor="w", text_color="#2b82c9" if type_log == "PERF" else "#e67e22").grid(row=ligne_idx, column=1, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.zone_tableau, text=user_log, width=110, anchor="w", text_color="#2ecc71").grid(row=ligne_idx, column=2, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.zone_tableau, text=description, width=500, anchor="w", text_color=couleur_ligne).grid(row=ligne_idx, column=3, padx=5, pady=2, sticky="w")

            ligne_idx += 1

        if ligne_idx == 1:
            ctk.CTkLabel(self.zone_tableau, text="Aucun log ne correspond à ces critères croisés.", text_color="gray").grid(row=1, column=0, columnspan=4, pady=25)

    def sauvegarder_fichier_config(self):
        with open(FICHIER_CONFIG_JSON, "w", encoding="utf-8") as f: json.dump(self.config_data, f, indent=4)

    def nettoyer_fenetre(self):
        for widget in self.winfo_children(): widget.destroy()

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
