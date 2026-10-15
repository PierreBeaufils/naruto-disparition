#!/bin/bash
# Lance VanishCam avec ses messages dans le Terminal (comme la version Windows).
# Les options sont transmises, ex. : --mode naruto --gesture-debug
for APP in "/Applications/VanishCam.app" "$(dirname "$0")/VanishCam.app" "$(dirname "$0")/dist/VanishCam.app"; do
  if [ -x "$APP/Contents/MacOS/VanishCam" ]; then
    exec "$APP/Contents/MacOS/VanishCam" "$@"
  fi
done
echo "VanishCam.app introuvable. Copiez-la dans le dossier Applications."
read -r -p "Appuyez sur Entrée pour fermer."
