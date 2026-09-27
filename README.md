Weather ETL Pipeline 🌦️
Pipeline de données météo pour Paris et Dakar, développé avec Python et orchestré par Apache Airflow.
Les données sont récupérées depuis l’API Open-Meteo, validées et stockées dans PostgreSQL. Logstash traite les fichiers JSON pour les envoyer à Elasticsearch, puis Kibana permet de visualiser et comparer les températures des deux villes.
L’environnement est conteneurisé avec Docker Compose.
