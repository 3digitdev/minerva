FROM mongo:latest

# Copy Minerva files
WORKDIR /usr/src/minerva
COPY initMongo.js ./

# General setup
CMD mongo initMongo.js && \
	apt-get -y update && \
	apt-get install -y systemd && \
	apt-get install -y logrotate

# TODO
# WHAT DO I DO HERE?
#ENTRYPOINT [""]


# docker run --detach --name=minerva-db -v ~/
# https://docs.docker.com/engine/reference/builder/