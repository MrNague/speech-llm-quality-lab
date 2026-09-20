# Guide d’annotation — pilote français, version 1.0

Objectif : obtenir 30 prises vérifiées de 3 à 20 secondes, cinq par catégorie. Lire `PILOT_RECORDING_SHEET.md`. Les textes sont fictifs et tous les cas sont DEV. Aucun enregistrement n'est encore fourni ou déclaré approuvé.

## Enregistrer

Pièce calme, microphone stable, distance constante, voix naturelle. Fermer les applications bruyantes. Dire la phrase une seule fois, sans prononcer son identifiant. Une prise par fichier, pas de données personnelles. Le script produit du WAV PCM16 mono 16 kHz et ne remplace jamais une prise existante.

Commencer avec PILOT001, PILOT006, PILOT011, PILOT016, PILOT021 et PILOT026 (une catégorie chacun), puis les quatre suivants du plan pour le diagnostic de dix audios. Le pilote complet comporte les 30 cas. La sélection de `run --limit 10` suit l'ordre du manifeste, pas cet ordre d'enregistrement : ce sous-ensemble sert au diagnostic matériel, jamais à comparer les catégories.

La durée par défaut est 12 s; l'ajuster entre 3 et 20 s selon la phrase. Éviter de longues plages de silence. Si la phrase est coupée, archiver la prise dans `data/local/archive/` puis réenregistrer. Les versions précédentes restent locales.

## Première écoute

Ouvrir le WAV dans le lecteur audio Windows. Écrire uniquement ce qui est audible. Le texte du plan n'est pas une transcription automatique ni une référence validée.

- Garder accents, élisions et négations audibles. Ne pas ajouter « ne » dans « j’arrive pas ».
- Garder « euh », « ben » et les répétitions audibles avec une orthographe constante.
- Conserver les erreurs réellement prononcées; si elles rendent la demande inexploitable, refaire la prise.
- Utiliser une ponctuation simple et lisible. Elle reste visible dans la métrique brute.
- Pour ce pilote, transcrire les nombres en lettres comme prononcés : « dix-huit heures », « quatre cent trois ». Conserver VPN, HTTP, USB et Wi-Fi comme termes conventionnels. Pour les lettres épelées : « A B douze ».
- La normalisation ne rend pas « huit » équivalent à « 8 ». Les équivalences sémantiques de nombres seront contrôlées séparément par les slots, pas masquées dans WER.
- Si deux lectures restent plausibles, choisir `unclear`. Ne pas inventer une référence certaine.

## Deuxième écoute

Effectuer une seconde session à un autre moment, sans consulter sa réponse précédente avant de saisir la nouvelle transcription. Le script demande explicitement cette confirmation. Une référence inchangée et une seconde écoute indépendante dans le temps permettent `approved`. Une correction remet le cas en attente et nécessite une nouvelle vérification.

Il s'agit de self-review par Pascal, pas d'accord entre deux annotateurs. Les dates, reviewer_id, empreintes et anciennes décisions sont conservés dans `reviews.json`. Le programme ne peut pas vérifier que l'écoute a réellement eu lieu : la confirmation du reviewer constitue la preuve déclarative.

Pour le futur corpus de 120 cas, au moins 24 seront revus à l'aveugle; ce contrôle final n'est pas remplacé par les vérifications de ce pilote.

## Catégories et erreurs

La catégorie principale est fixée par le plan; des erreurs peuvent relever de plusieurs catégories. Une paire d'homophones n'est pas prouvée par une simple différence de caractères. Distinguer erreur de référence, erreur ASR, effet de normalisation et incertitude. Annoter manuellement les différences d'heure, de négation et d'identifiant avant toute conclusion.

Le pilote développe les règles : tous ses cas et leurs paraphrases restent en DEV. En AP3, planifier les nouveaux groupes et les 30 cas TEST séparément. Ne pas changer ces cas en TEST après avoir utilisé leurs résultats.

Publication : `publication_allowed=false`. Les audios, références locales et résultats restent dans les répertoires exclus de Git.
