# Naruto Disparition — VanishCam pour macOS

Une webcam à effets spéciaux pour Mac. Joignez les paumes devant la caméra et
vous disparaissez dans un nuage de fumée, remplacé par un rondin de bois, comme
la technique de substitution de Naruto. L'effet passe dans Microsoft Teams (et
toute autre app de visio) grâce à la caméra virtuelle d'OBS.

Le traitement vidéo se fait entièrement sur le Mac : rien n'est enregistré ni
envoyé à un serveur. L'image envoyée en visio ne contient que la vidéo et
l'effet, sans texte ni menu par-dessus.

## Crédits

Ce projet est un portage macOS de
[vanish_webcam](https://github.com/Nicovic17/vanish_webcam) de Nicovic17,
application Windows d'origine. La détection des gestes, l'effet de fumée, le
rondin et le son viennent de ce projet. Le rondin est une illustration
originale de l'auteur ; aucune image de l'anime n'est incluse.

## Les deux effets

**Naruto Vanish.** Joignez les paumes devant la webcam, doigts côte à côte et
non entrelacés, les deux mains bien visibles. Une demi-seconde après la
détection (le temps que le geste soit vu à l'image), le son se déclenche, vous
disparaissez dans la fumée et un rondin tombe à votre place. Il reste affiché
jusqu'à ce que vous appuyiez sur `R`.

**Normal Vanish.** Levez l'index et le majeur en V : vous vous dissolvez
progressivement en 3,6 secondes environ.

Dans les deux cas, l'app ne « gomme » pas la personne en temps réel : elle
affiche à sa place une image du décor vide, capturée au démarrage. C'est
pourquoi la capture du fond est importante (voir plus bas).

## Compatibilité

- Mac Apple Silicon (M1 ou plus récent). MediaPipe, utilisé pour détecter les
  mains, n'existe pas pour les Mac Intel.
- macOS 13 Ventura ou plus récent.
- OBS Studio 30 ou plus récent pour la caméra virtuelle (Teams, Zoom, Meet…).
  Sans OBS, l'app fonctionne quand même, mais seulement dans sa fenêtre
  d'aperçu.

## Installation

### 1. Construire l'app (une fois)

Prérequis : Python 3.10 à 3.13, à installer depuis
[python.org](https://www.python.org/downloads/macos/).

Dans le Terminal, depuis le dossier du projet :

```bash
bash BUILD_MACOS.sh
```

Le script crée un environnement Python dédié (`.venv-build`), installe les
dépendances, télécharge les modèles MediaPipe, construit `dist/VanishCam.app`,
la signe, lance un auto-test et crée `dist/VanishCam.dmg`. Le premier build
prend quelques minutes, les suivants sont rapides.

### 2. Installer l'app

Ouvrez `dist/VanishCam.dmg` et glissez **VanishCam** dans **Applications**.

L'app n'est pas notarisée par Apple. Au premier lancement : clic droit sur
VanishCam → **Ouvrir** → **Ouvrir**. Si macOS refuse, allez dans Réglages
Système → Confidentialité et sécurité → **Ouvrir quand même**.

Autorisez ensuite l'accès à la caméra quand macOS le demande.

### 3. Préparer OBS (une fois)

1. Installez [OBS Studio](https://obsproject.com/).
2. Ouvrez OBS, cliquez sur **Démarrer la caméra virtuelle**, puis arrêtez-la.
   Autorisez l'extension système si macOS le demande.
3. Fermez OBS.

VanishCam alimente ensuite la caméra virtuelle d'OBS sans qu'OBS soit ouvert.
OBS ne doit pas diffuser sa propre caméra virtuelle en même temps.

## Utilisation

1. Lancez **VanishCam**.
2. Choisissez l'effet dans le menu : clic sur **Normal Vanish** ou **Naruto
   Vanish**, ou touches `1` / `2`.
3. **Sortez complètement du champ** pendant la capture du fond. Le titre de la
   fenêtre affiche « STEP OUT OF FRAME » et un compte à rebours de 4 secondes.
   Revenez quand le titre redevient « Webcam - Preview ».
4. Faites le geste.

### Dans Microsoft Teams

Paramètres → Périphériques → Caméra → **OBS Virtual Camera**. Vous pouvez aussi
choisir la caméra depuis l'écran de prévisualisation avant de rejoindre une
réunion. Lancez VanishCam avant d'activer votre caméra dans Teams.

## Raccourcis clavier

Les touches ne fonctionnent que lorsque la fenêtre de VanishCam est active.
Pendant un appel, cliquez d'abord sur la fenêtre d'aperçu.

**Menu de démarrage**

| Touche | Action |
|---|---|
| `1` | Lancer Normal Vanish |
| `2` | Lancer Naruto Vanish |
| `Q` ou `Échap` | Quitter |

**Pendant l'utilisation**

| Touche | Action |
|---|---|
| `Espace` | Refaire la capture du fond (sortez du champ 4 secondes) |
| `R` | Réapparaître (retire le rondin, le geste est de nouveau détecté) |
| `V` | Déclencher l'effet manuellement, sans geste ni délai |
| `F` | Activer ou désactiver le plein écran |
| `Q` ou `Échap` | Quitter et libérer la webcam |

## Options de lancement

Pour voir les messages en direct ou passer des options, utilisez
`Lancer VanishCam (Terminal).command` (double-clic, ou depuis le Terminal) :

```bash
"./Lancer VanishCam (Terminal).command" --mode naruto --gesture-debug
```

| Option | Effet |
|---|---|
| `--mode naruto` / `--mode normal` | Démarrer directement un effet, sans menu |
| `--camera 1` | Utiliser une autre webcam (0 par défaut) |
| `--width 1280 --height 720` | Résolution vidéo (960×540 par défaut) |
| `--fps 30` | Images par seconde maximum envoyées à la caméra virtuelle |
| `--fullscreen` | Démarrer en plein écran |
| `--no-mirror` | Ne pas inverser l'image en miroir |
| `--no-virtual-camera` | Aperçu local uniquement, sans caméra virtuelle |
| `--virtual-camera` | Exiger la caméra virtuelle (erreur si OBS est absent) |
| `--virtual-device NOM` | Nom du périphérique virtuel à utiliser |
| `--gesture-debug` | Afficher dans le Terminal ce que voit la détection des mains |
| `--help` | Afficher l'aide |

## Conseils et dépannage

**Je reste visible en transparence après la disparition.** Vous étiez dans le
champ pendant la capture du fond, et vous avez été enregistré dans le décor.
Appuyez sur `Espace`, sortez complètement du champ et attendez que le titre de
la fenêtre redevienne normal. Refaites aussi la capture si la lumière change ou
si vous bougez la caméra.

**Le geste n'est pas détecté.** Gardez les deux mains entières dans l'image,
paumes collées et doigts côte à côte (pas entrelacés). Lancez l'app avec
`--gesture-debug` pour voir en direct le nombre de mains détectées.

**Teams ne montre pas l'effet.** Vérifiez que **OBS Virtual Camera** est
sélectionnée dans Teams, que VanishCam est lancée et qu'OBS ne diffuse pas sa
propre caméra virtuelle.

**Le son.** Il est joué par les haut-parleurs du Mac. Les autres participants
ne l'entendront que s'il est capté par votre micro, et la suppression de bruit
de Teams peut le couper.

**La webcam ne s'ouvre pas.** Réglages Système → Confidentialité et sécurité →
Caméra : autorisez VanishCam. Fermez les autres apps qui utilisent la webcam.

**Les messages de l'app.** Lancée depuis le Finder, l'app écrit ses messages
dans `~/Library/Logs/VanishCam/vanishcam.log` et affiche les plus importants en
notification.

**Plantage « Check failed: service_ Service is unavailable » au build.**
MediaPipe 1.0.1 a un bug sur macOS. Le projet utilise la 1.0.0 ; vérifiez
`requirements.txt`, puis réinstallez avec
`.venv-build/bin/python -m pip install -r requirements.txt`.

## Réglages

Le délai entre la détection des paumes jointes et le déclenchement de l'effet
se règle en haut de `vanish_cam.py` :

```python
NARUTO_TRIGGER_DELAY_SECONDS = 0.5
```

Relancez `bash BUILD_MACOS.sh` après toute modification.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `vanish_cam.py` | Application principale : menu, capture, détection des gestes, effets, caméra virtuelle |
| `naruto_effect.py` | Fumée procédurale et chute du rondin |
| `vanish_sound.py` | Lecture du son |
| `macos_support.py` | Spécifique au Mac : log, notifications, boîte d'erreur |
| `hand_landmarker.task`, `face_landmarker.task` | Modèles MediaPipe |
| `assets/` | Rondin, son, icônes |
| `requirements.txt` | Dépendances Python |
| `VanishCam_macos.spec` | Recette PyInstaller de l'app |
| `BUILD_MACOS.sh` | Script de build complet (app + DMG) |
| `Lancer VanishCam (Terminal).command` | Lancement avec messages et options |
| `test_*.py` | Tests automatiques |
| `run3.py` | Ancien script du projet d'origine, non utilisé par l'app |

Les modèles `gesture_recognizer.task` et `selfie_segmenter_landscape.tflite`
(mode Normal) sont téléchargés dans `models/` au moment du build.

### Lancer les tests

Les tests importent le code sous le nom de paquet `local_app` (héritage du
projet d'origine) :

```bash
.venv-build/bin/python -m pip install pytest
mkdir -p /tmp/vanish-tests && ln -sfn "$PWD" /tmp/vanish-tests/local_app
(cd /tmp/vanish-tests && "$OLDPWD/.venv-build/bin/python" -m pytest local_app)
```

Deux tests du mode Normal (`MultiViewTests`) échouent déjà dans le projet
d'origine ; ils ne concernent pas le mode Naruto.

## Différences avec la version Windows

- Capture webcam via AVFoundation, avec attente de l'autorisation caméra au
  premier lancement.
- Compte à rebours de capture du fond dans le titre de la fenêtre (il n'y a pas
  de console visible sur Mac).
- Notifications macOS, fichier de log et boîte d'erreur.
- Textes de l'application en anglais.
- Délai de 0,5 seconde avant l'effet Naruto, pour que le geste soit visible.
- MediaPipe 1.0.0 au lieu de 1.0.1 (bug macOS).
- Build en `.app` et `.dmg` au lieu d'un `.exe`.
