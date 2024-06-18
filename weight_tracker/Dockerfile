# Utiliser une image de base officielle de Python
FROM python:3.10-slim

# Installer les dépendances
RUN apt-get update && apt-get install -y nginx certbot python3-certbot-nginx

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le contenu du répertoire actuel dans le répertoire de travail
COPY . /app
WORKDIR /app

# Configurer Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Exposer les ports sur lesquels l'application sera exécutée
EXPOSE 80 443

# Définir la commande à exécuter lorsque le conteneur démarre
CMD service nginx start && certbot --nginx -n --agree-tos --email lupia1337@gmail.com -d groslardemer.de -d www.groslardemer.de && python app.py
