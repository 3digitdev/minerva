FROM mongo:latest

# Install Python and Python Accessories
RUN apt-get update \
	&& apt-get install -y software-properties-common \
	&& add-apt-repository -y ppa:deadsnakes/ppa \
	&& apt-get install -y python3.8 python3-pip

# Copy Minerva files
WORKDIR /usr/src/app
COPY minerva/ ./minerva/
COPY requirements.txt *.py Makefile minerva_config.json pyproject.toml ./

# Set things up
RUN mongod &
RUN make init && make flask run