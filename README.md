# RailData Backend

## Configuration

Il faut spécifier la variable d'environnement `allow_origins` avec le domaine du client frontend
qui sera autorisé à faire des requêtes. Dans un environnement de développement, on peut faire un
fichier `.env` avec la valeur `allow_origins="*"`.

Un dossier `static` est nécessaire, ça peut être un montage vers un volume ou simplement
un dossier vide pour le développement : il contiendra le fichier `viarail.sqlite` qui sera
automatiquement construit si vide.

## Développement en local sans Docker

- Faire `poetry install` pour installer les dépendances.
- Pour lancer le serveur : `poetry run uvicorn api:app --reload` (la dernière option est
  pour le développement, pour recharger le serveur automatiquement lors d'une modification du code).

## Avec Docker

- Construire l'image : `docker build -t hyakosm/raildata-backend .`
- Démarrer le container (par exemple en local sur le port 8000) : `docker run -p 8000:8000 -e allow_origins='*' -d --rm hyakosm/raildata-backend`

## Mise à jour des données GTFS

Le script `update_gtfs_data.py` est à exécuter manuellement pour cela :
`poetry run ./update_gtfs_data.py`

## Sources des données

- Données en temps réel : https://tsimobile.viarail.ca/index-fr.html
- Données GTFS : https://www.viarail.ca/fr/ressources-developpeurs
