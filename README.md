# Scripts à exécuter en tâche planifiée (cron)

Les scripts suivants servent à alimenter un fichier de base de données SQLite. Si le fichier n'existe pas il sera créé sous le nom `viarail.sqlite`.

## update_gtfs_data.py

Récupère les informations statiques depuis les données ouverts GTFS de Via Rail et met à jour le fichier de base de données.
À planifier de temps en temps ou à exécuter manuellement au gré des besoins.

Informations officielles ici : https://www.viarail.ca/fr/ressources-developpeurs

## get_late_trains.py

Récupère les temps des trains de la journée depuis l'API destinée aux informations voyageur en temps réel et les ajoute au fichier de base de données. Les trains arrivés peuvent être retirés de l'API au bout de quelques heures, il vaut mieux exécuter ce script une fois par heure pour être tranquille.

Source des données ici : https://tsimobile.viarail.ca/index-fr.html
