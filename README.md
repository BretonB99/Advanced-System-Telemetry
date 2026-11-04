# 🛡️ Advanced System Telemetry (v1.0.1)

Une solution de supervision locale et d'administration système asynchrone, légère, modulaire et entièrement sécurisée pour Windows.

La version v1.0.1 apporte une amélioration majeure de l'ergonomie et de la précision de configuration : **les curseurs et barres graphiques ont été intégralement remplacés par des champs de saisie de texte numériques au clavier**. L'administrateur peut désormais définir à la seconde près les intervalles de capture et la taille limite des journaux de rapports.

---

## 🚀 Fonctionnalités Clés & Capteurs Intégrés

Le logiciel s'appuie sur une architecture asynchrone non bloquante (`asyncio`) capable de suivre plusieurs indicateurs système critiques en simultané avec une empreinte matérielle inférieure à 1% de CPU :

*   **Surveillance des Applications (`APPLICATIONS`) :** Détection instantanée (à 0,1s près) de l'ouverture et de la fermeture de chaque logiciel. Capture le nom du processus, son PID et l'utilisateur exact qui a lancé l'application.
*   **Flux de Performances (`PERF`) :** Mesure en continu de la charge globale du processeur (CPU %) et de l'utilisation de la mémoire vive (RAM %) pour identifier les ralentissements.

---

## 🔒 Sécurité & Robustesse Professionnelle

- **Champs de Saisie Numériques Précis :** Plus de approximations liées aux curseurs graphiques. Saisissez directement au clavier l'intervalle en secondes souhaité.
- **Double Format d'Écriture (Texte + JSON) :** Génère simultanément un fichier `.log` clair pour la lecture humaine et un flux structuré au format NDJSON (`.json`) idéal pour l'analyse automatisée par script ou SIEM.
- **Sécurité Native Windows (DACL/ACL NTFS) :** Les répertoires de stockage dans `ProgramData` suppriment l'héritage système. Seuls le compte Système et le groupe Administrateurs possèdent les droits de lecture et d'écriture. Les utilisateurs surveillés reçoivent un "Accès Refusé".
- **Hachage Cryptographique :** Le mot de passe d'accès au Dashboard est sécurisé via une empreinte mathématique irréversible **SHA-256**.
- **Gestionnaire de Rotation GZIP :** Dès qu'un fichier de log dépasse la taille limite définie au clavier par l'administrateur, il est automatiquement archivé et compressé au format `.gz` en arrière-plan pour économiser l'espace disque.

---

## 📂 Architecture du Projet (v1.0.1)

```text
Advanced-System-Telemetry/
│
├── Code Source
│   ├── main.pyw                 # Le moteur de capture invisible d'arrière-plan (Asyncio)
│   ├── dashboard.pyw            # L'interface graphique d'administration avec saisie clavier (CustomTkinter)
│   ├── config.py                # Configuration des variables et chemins locaux uniques
│   ├── security.py              # Gestion du démarrage auto et des droits NTFS de la machine
│   ├── writer.py                # Moteur d'écriture double et de compression GZIP asynchrone
│   └── capteurs/                # Modules de surveillance indépendants (Package Python)
│       ├── __init__.py          # Fichier d'initialisation (vide)
│       ├── performance.py       # Capteur de charge CPU / RAM
│       └── applications.py      # Capteur de suivi des processus utilisateurs
│
├── License                      # Fichier légal de la Licence MIT
└── README.md                    # La présente documentation technique
```

---

## 🛠️ Installation et Déploiement

### Option 1 : Utiliser l'installateur autonome (Recommandé)
1. Allez dans l'onglet **Releases** à droite de ce dépôt GitHub.
2. Téléchargez le fichier unique `telemetry_setup.exe`.
3. Lancez-le en mode Administrateur : il déploie le service d'arrière-plan, configure la persistance au démarrage et crée votre raccourci personnalisé dans le menu Démarrer.

### Option 2 : Exécution via les sources Python
```bash
pip install customtkinter psutil pywin32
```
Lancez ensuite `dashboard.pyw` pour configurer votre mot de passe, puis `main.pyw` pour démarrer la capture.

---

## ✍️ Un petit mot de l'auteur

Ce projet est né de ma volonté de créer un outil transparent, où toutes les données restent stockées localement, sous le contrôle exclusif de l'administrateur, sans aucune exfiltration extérieure. L'intégration de la saisie au clavier dans cette version v1.0.1 répond aux retours d'expérience pour offrir un contrôle chirurgical de la télémétrie.

Si cet outil vous est utile dans vos tâches d'administration, n'hésitez pas à laisser une ⭐️ sur ce dépôt !

---

## 📄 Licence
Ce projet est distribué gratuitement sous les termes de la **Licence MIT**.
