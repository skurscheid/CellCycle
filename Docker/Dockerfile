# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:0.11

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
WORKDIR /app
RUN apt-get clean
RUN apt-get update 
RUN apt-get install -y --fix-missing --no-install-recommends \
    unzip \
    build-essential \
    wget \
    make \ 
    bzip2 \
    libncurses5-dev \
    zlib1g-dev \ 
    libbz2-dev \
    software-properties-common
RUN wget https://repo.continuum.io/miniconda/Miniconda3-3.7.0-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p /app/miniconda
ENV PATH "/app/miniconda/bin:$PATH"

RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
