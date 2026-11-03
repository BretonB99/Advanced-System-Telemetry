# 🛡️ Advanced System Telemetry

Une solution de supervision locale et d'administration système asynchrone, légère, modulaire et entièrement sécurisée pour Windows. 

Ce logiciel fonctionne de manière transparente en arrière-plan sans interface visuelle pour l'utilisateur de la session, et met à disposition de l'administrateur un panneau de contrôle moderne (style Windows 11 Dark Mode) protégé par mot de passe avec une visionneuse de logs en temps réel.

---

## 🚀 Fonctionnalités Clés & Capteurs Intégrés

Le logiciel s'appuie sur une architecture asynchrone non bloquante (`asyncio`) capable de suivre une douzaine d'indicateurs système critiques en simultané avec une empreinte matérielle inférieure à 1% de CPU :

### 🎛️ Capteurs Natifs (Inclus et actifs par défaut)
*   **Surveillance des Applications (`APPLICATIONS`) :** Détection instantanée (à 0,1s près) de l'ouverture et de la fermeture de chaque logiciel. Capture le nom du processus, son PID et l'utilisateur exact qui a lancé l'application.
*   **Flux de Performances (`PERF`) :** Mesure en continu et à intervalle régulier de la charge globale du processeur (CPU %) et de l'utilisation de la mémoire vive (RAM %) pour identifier les ralentissements.

### 🔌 Capteurs Réseau & Connectivité (Architecture Évolutive)
*   **Bande Passante & Volumes :** Calcul précis des Mo/Go téléchargés et téléversés par la machine pour repérer les surconsommations de données réseau.
*   **Stabilité Internet (Ping) :** Envoi de requêtes automatisées ultra-légères vers un serveur stable pour mesurer la latence et journaliser les micro-coupures internet.
*   **Connexions Actives (Sockets) :** Cartographie en direct des ports réseau ouverts et des adresses IP externes contactées par les logiciels en arrière-plan.

### 💾 Matériel & Maintenance Préventive (Architecture Évolutive)
*   **Espace Stockage :** Suivi dynamique de l'espace libre restant (en Go et en %) sur l'ensemble des disques durs (`C:`, `D:`, etc.) pour anticiper les plantages liés à un disque saturé.
*   **Santé du Matériel (Thermique) :** Lecture en temps réel des sondes de températures internes du processeur (CPU) et de la carte graphique (GPU).
*   **Gestion Énergétique :** Suivi du niveau de batterie (pour les PC portables), de l'état de charge (secteur/batterie) et calcul de l'autonomie restante.

### ⏰ Sessions & Activité Utilisateur (Architecture Évolutive)
*   **Temps d'Activité (Uptime) :** Enregistrement de l'horodatage exact du dernier démarrage de Windows et calcul de la durée d'activité continue du système.
*   **Détecteur d'Inactivité (Idle Time) :** Calcul du temps écoulé depuis la dernière action physique sur la souris ou le clavier pour analyser la présence réelle de l'utilisateur.
*   **Gestion des Sessions Actives :** Journalisation du nombre et du nom des sessions Windows ouvertes en simultané (utilisateurs locaux et connexions à distance RDP).
*   **Suivi des Périphériques USB :** Journalisation instantanée du branchement et du débranchement des clés USB, disques externes ou périphériques amovibles.

---

## 🔒 Sécurité & Robustesse Professionnelle

- **Double Format d'Écriture (Texte + JSON) :** Génère simultanément un fichier `.log` clair pour la lecture humaine et un flux structuré au format NDJSON (`.json`) idéal pour l'analyse automatisée par script ou SIEM.
- **Sécurité Native Windows (DACL/ACL NTFS) :** Les répertoires de stockage dans `ProgramData` suppriment l'héritage système. Seuls le compte Système et le groupe Administrateurs possèdent les droits de lecture et d'écriture. Les utilisateurs surveillés reçoivent un "Accès Refusé".
- **Hachage Cryptographique :** Le mot de passe d'accès au Dashboard n'est jamais stocké en clair. Il est sécurisé via une empreinte mathématique irréversible **SHA-256**.
- **Gestionnaire de Rotation GZIP :** Dès qu'un fichier de log dépasse la taille limite définie par l'administrateur dans l'interface, il est automatiquement archivé et compressé au format `.gz` en arrière-plan pour économiser l'espace disque.

---

## 📂 Architecture Finale du Projet

L'arborescence complète du projet pré-compilation est organisée de la manière suivante dans vos répertoires :

```text
Advanced-System-Telemetry/
│
├── Code Source
│   ├── main.pyw                 # Le moteur de capture invisible d'arrière-plan (Asyncio)
│   ├── dashboard.pyw            # L'interface graphique d'administration (CustomTkinter)
│   ├── config.py                # Configuration des variables et chemins locaux uniques
│   ├── security.py              # Gestion du démarrage auto et des droits NTFS de la machine
│   ├── writer.py                # Moteur d'écriture double et de compression GZIP asynchrone
│   └── capteurs/                # Modules de surveillance indépendants (Package Python)
│       ├── __init__.py          # Fichier d'initialisation (vide)
│       ├── performance.py       # Capteur de charge CPU / RAM
│       └── applications.py      # Capteur de suivi des processus utilisateurs
│
├── License
└── README.md
```

---

## 🛠️ Installation et Déploiement

### Option 1 : Utiliser l'installateur autonome (Recommandé)
1. Allez dans l'onglet **Releases** à droite de ce dépôt GitHub.
2. Téléchargez le fichier unique `telemetry_setup.exe`.
3. Lancez-le en mode Administrateur : il déploie le service d'arrière-plan, configure la persistance au démarrage et crée votre raccourci personnalisé avec icône dédiée dans le menu Démarrer.

### Option 2 : Exécution via les sources Python
Si vous préférez exécuter le code manuellement, installez les dépendances requises :
```bash
pip install customtkinter psutil pywin32
```
Lancez ensuite `dashboard.pyw` pour configurer votre mot de passe et vos curseurs, puis `main.pyw` pour démarrer le moteur de capture en tâche de fond.

---

## ✍️ Un petit mot de l'auteur

Ayant souvent eu besoin d'un outil de supervision simple, rapide et qui ne s'accapare pas toutes les ressources de la machine, j'ai décidé de concevoir *Advanced System Telemetry*. 

Ce projet est né de ma volonté de créer un outil transparent, où toutes les données restent stockées localement, sous le contrôle exclusif de l'administrateur, sans aucune exfiltration extérieure. Je le partage aujourd'hui gratuitement en Open Source pour, je l'espère, simplifier la maintenance et le suivi de vos postes Windows au quotidien.

Ce logiciel a été développé dans l'objectif d'allier les performances de l'asynchronisme à la structure du format JSON pour le traitement informatique. C'est un projet personnel que j'ai plaisir à offrir à la communauté. Si cet outil vous est utile dans vos tâches d'administration, n'hésitez pas à laisser une ⭐️ sur ce dépôt, cela fait toujours plaisir et aide à faire connaître le projet !

Bon déploiement, et merci pour votre confiance !

---

## 📄 Licence
Ce projet est distribué gratuitement sous les termes de la **Licence MIT**. Vous êtes libre de l'utiliser, de le modifier et de le partager à des fins personnelles ou professionnelles.
