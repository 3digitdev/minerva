FROM bitnami/python:3.8

# Copy Minerva files
WORKDIR /usr/src/app
COPY minerva/ ./minerva/
COPY requirements.txt *.py Makefile minerva_config.json pyproject.toml ./
COPY startFlask.sh /usr/bin/startFlask.sh
RUN chmod +x /usr/bin/startFlask.sh

ENTRYPOINT ["startFlask.sh"]

# docker run --detach --name=minerva-api -p 5000:5000 minerva-api
# https://docs.docker.com/engine/reference/builder/