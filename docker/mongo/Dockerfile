FROM mongo:latest

WORKDIR /usr/src/minerva

COPY initMongo.js ./
COPY setupMongoDocker.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/setupMongoDocker.sh

ENTRYPOINT ["setupMongoDocker.sh"]

# docker run --detach --name=minerva-db -v ~/
# https://docs.docker.com/engine/reference/builder/