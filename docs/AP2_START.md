# AP2 — démarrage sous Windows

État : outils et plan disponibles. Les 30 enregistrements réels, leur validation et le rapport ASR sur le Celeron restent à produire. AP2 n'est pas encore terminé.

## 1. Mettre à jour le projet

Depuis `quality-lab-work` :

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -r requirements-asr.lock
.\.venv\Scripts\python.exe -m pytest -q -rs
```

La dépendance ASR est optionnelle pour les tests. L'installation Windows et les performances sur le N5100 doivent encore être vérifiées. Ne pas activer CUDA pour Intel UHD. Si une commande échoue, conserver le message exact et arrêter cette séquence.

## 2. Enregistrer une première prise

Lire `ANNOTATION_GUIDE.md` puis `PILOT_RECORDING_SHEET.md`.

```powershell
.\.venv\Scripts\python.exe scripts/record_pilot.py --case PILOT001 --seconds 12
```

Appuyer sur Entrée lorsque le microphone est prêt, puis lire la phrase affichée. Le script utilise le microphone par défaut. Si le périphérique refuse 16 kHz mono, signaler son erreur avant de changer le format; ne pas renommer un MP3 en WAV.

Écouter `data/local/pilot/audio/PILOT001.wav`. Ensuite :

```powershell
.\.venv\Scripts\python.exe scripts/review_pilot.py --case PILOT001 --reviewer pascal
```

Saisir la transcription réelle. La première passe reste pending. Refaire l'écoute et la commande à un autre moment pour confirmer approved. Aucun texte n'est approuvé par simple génération. Répéter pour les autres cas. Le manifeste ne contient que les cas ayant eu une revue; sa taille n'est pas une preuve des 30 cas terminés.

## 3. Préparer le modèle local

Candidat : Systran/faster-whisper-tiny, multilingue, CPU int8, beam_size=1, quatre threads. E02 reste provisoire jusqu'au test réel.

```powershell
.\.venv\Scripts\python.exe scripts/download_asr_model.py
```

Cette commande télécharge les poids depuis Hugging Face et fige leur révision; elle n'envoie aucun audio. Le modèle est sous licence MIT selon sa fiche source. Le téléchargement et les dépendances nécessitent le réseau. Les inférences ultérieures sont locales.

## 4. Diagnostic puis pilote

Tous les cas présents dans le manifeste doivent être approved et DEV. Commencer avec un cas, puis dix, avant les trente :

```powershell
.\.venv\Scripts\python.exe -m quality_lab validate --config configs/pilot.json
.\.venv\Scripts\python.exe -m quality_lab run --config configs/pilot.json --limit 1
.\.venv\Scripts\python.exe -m quality_lab run --config configs/pilot.json --limit 10
.\.venv\Scripts\python.exe -m quality_lab run --config configs/pilot.json
```

Chaque commande run crée un UUID neuf. Les résultats sont dans `runs/UUID/` : run.json, inputs.jsonl, predictions.jsonl, metrics.json, report.html. Ouvrir report.html dans le navigateur. Aucun résultat réel n'est prérempli.

Le chargement du modèle a une limite provisoire de 180 s, chaque transcription de 120 s. Un timeout arrête le worker et marque les cas restants skipped. Trois erreurs d'inférence consécutives arrêtent aussi le traitement. Les échecs réduisent la coverage, jamais le nombre de cas planifiés. Pas de reprise ni de cache dans ce pilote : ces fonctions sont prévues en AP3. Une nouvelle invocation ne modifie pas les runs précédents.

Le rapport affiche WER et CER bruts/normalisés, leurs nombres d'erreurs et dénominateurs, coverage, RTF hors chargement et RSS observée après les cas. RSS observée n'est pas la consommation mémoire maximale. Pour le diagnostic matériel, observer aussi la mémoire dans le Gestionnaire des tâches. Pas de score de slot tant que l'extracteur et la confirmation manuelle ne sont pas implémentés.

## 5. Fin d'AP2

Exiger 30 prises approuvées (cinq par catégorie), le guide appliqué, les hand-tests réussis et un rapport réel reproductible. Le diagnostic matériel préalable est distinct du benchmark final. Un résultat de fixture ne remplace jamais ces preuves.

Sources techniques consultées :
- https://github.com/SYSTRAN/faster-whisper
- https://opennmt.net/CTranslate2/hardware_support.html
- https://huggingface.co/Systran/faster-whisper-tiny
