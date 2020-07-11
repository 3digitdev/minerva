FROM bitnami/mongodb:latest

# Copy Minerva files
WORKDIR /usr/src/minerva
COPY initMongo.js ./

CMD mongo initMongo.js

# TODO
ENTRYPOINT [""]


# docker run --detach --name=minerva-db -v ~/
# https://docs.docker.com/engine/reference/builder/