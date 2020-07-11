FROM bitnami/python:3.8

# Copy Minerva files
WORKDIR /usr/src/app
COPY minerva/ ./minerva/
COPY requirements.txt *.py Makefile minerva_config.json pyproject.toml ./

# TODO
# make init && make flask_run
ENTRYPOINT [""]


# docker run --detach --name=minerva-api -p 5000:5000 minerva-api