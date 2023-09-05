FROM python:3.7-slim

# Télécharge et installe Blender 2.93.1 pour Windows
ADD https://download.blender.org/release/Blender3.0/blender-3.0.0-windows-x64.zip C:\\blender.zip
RUN powershell -Command Expand-Archive -Path C:\\blender.zip -DestinationPath C:\\ && \
    del C:\\blender.zip


# Change le répertoire de travail
WORKDIR /app

# Crée un environnement virtuel et active-le
ENV VIRTUAL_ENV=/app/flask
ENV PATH="$VIRTUAL_ENV/Scripts:$PATH"

# Copie les fichiers de l'application dans le conteneur
COPY . /app/

# Définit l'entrée pour le conteneur
CMD ["python", "app.py"]
