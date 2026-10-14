# 👻 Screamer Bot

Un bot Discord qui permet de **lancer un screamer en plein écran** (image + son) et de **simuler l'appui sur une touche du clavier** sur l'ordinateur qui héberge le bot, le tout via des commandes slash.

> ⚠️ Ce bot agit directement sur la machine où il tourne. Lis la section [Sécurité](#-sécurité) avant de l'inviter quelque part.

---

## ✨ Fonctionnalités

| Commande | Description |
|----------|-------------|
| `/screamer image:<fichier> son:<fichier>` | Affiche l'image en plein écran et joue le son pendant 2 secondes |
| `/command touch:<touche>` | Fait appuyer le bot sur la touche de ton choix (ex : `z`, `space`, `enter`, `f5`) |

### Détails

- **`/screamer`**
  - Vérifie que le premier fichier est bien une image (`image/*`) et le second un audio (`audio/*`).
  - Les fichiers sont téléchargés dans des fichiers temporaires, puis supprimés après utilisation.
  - Un verrou (`asyncio.Lock`) empêche deux screamers de se lancer en même temps : ils sont mis en file d'attente.
  - Appuyer sur **Échap** pendant le screamer l'interrompt immédiatement.
  - Les réponses sont *éphémères* (visibles uniquement par l'utilisateur de la commande).
- **`/command`**
  - Utilise [`pyautogui.press`](https://pyautogui.readthedocs.io/) pour simuler l'appui sur une touche.
  - Les noms de touches valides sont ceux de `pyautogui.KEYBOARD_KEYS`.

---

## 📋 Prérequis

- Python **3.10+**
- Un environnement graphique (Windows, macOS ou Linux sous X11)
- Une application Discord avec un bot (voir [portail développeur](https://discord.com/developers/applications))

---

## 🚀 Installation

```bash
# 1. Récupérer le projet
git clone <url-du-repo>
cd <nom-du-repo>

# 2. (Optionnel) Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### `requirements.txt`

```
discord.py
pyautogui
pygame
python-dotenv
```

---

## ⚙️ Configuration

### 1. Créer le bot Discord

1. Va sur le [portail développeur Discord](https://discord.com/developers/applications) et crée une application.
2. Dans l'onglet **Bot**, génère un token.
3. Dans **OAuth2 → URL Generator**, coche les scopes :
   - `bot`
   - `applications.commands`
4. Utilise l'URL générée pour inviter le bot sur ton serveur.

Aucun *intent* privilégié n'est nécessaire (le bot utilise `Intents.default()`).

### 2. Fichier `.env`

Crée un fichier `.env` à la racine du projet :

```env
KEY=ton_token_discord_ici
```

> 🔒 Ne commit **jamais** ce fichier. Il est normalement dans `.gitignore` pour éviter ce genre de situations

---

## ▶️ Lancement

```bash
python bot.py
```

Au démarrage, les commandes slash sont synchronisées automatiquement (`setup_hook`). Elles peuvent mettre quelques minutes à apparaître sur Discord la première fois. Pour utiliser les commandes vous devez d'abord ajouter le bot a un serveur ou a vos applications.

---

## 💡 Utilisation

### Lancer un screamer

```
/screamer image:photo.png son:cri.mp3
```

### Appuyer sur une touche

```
/command touch:space
```

---

## 🔧 Personnalisation

- **Durée du screamer** : modifie le paramètre `duration` (en millisecondes) dans `screamer(photo, sound, duration=2000)`.
- **Touche par défaut** : `use_touch(touch="z")`.

---

## 🔐 Sécurité

Ce bot donne à quiconque peut utiliser ses commandes un contrôle partiel sur ton PC (affichage plein écran, son, simulation de clavier). Quelques recommandations :

- Ne l'invite que sur **un serveur privé** avec des personnes de confiance.
- Limite l'accès aux commandes via **Paramètres du serveur → Intégrations → ton bot** (permissions par rôle / salon).
- Tu peux aussi restreindre les commandes à toi seul en vérifiant `interaction.user.id` dans le code.
- Ne partage jamais ton token. S'il fuite, régénère-le immédiatement depuis le portail développeur.
- Évite de lancer le bot pendant que tu travailles sur quelque chose d'important : `/command` peut déclencher des raccourcis clavier indésirables.

---

## 🛠️ Dépannage

| Problème | Piste de solution |
|----------|-------------------|
| Les commandes n'apparaissent pas | Attends quelques minutes, vérifie le scope `applications.commands`, relance Discord |
| `Erreur : ...` après `/screamer` | Vérifie que le format image/audio est supporté par pygame (PNG, JPG, MP3, WAV, OGG) |
| Pas de son | Vérifie ton périphérique audio par défaut et le format du fichier |
| `/command` ne fait rien | Vérifie que le nom de la touche est valide pour pyautogui ; sur Linux, X11 est requis (Wayland n'est pas supporté) |
| Sur macOS, aucune touche ne passe | Autorise l'accessibilité pour ton terminal dans *Réglages Système → Confidentialité et sécurité* |

---

## 📄 Licence

MIT
