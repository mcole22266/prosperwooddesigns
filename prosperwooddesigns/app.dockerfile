# app.dockerfile
# Michael Cole
#
# Dockerfile for the app's Python container
# -----------------------------------------

FROM python:3.7.5-slim
LABEL maintainer="Michael Cole <mcole042891.prof.dev@gmail.com>"

# install awscli
RUN apt-get update && \
    apt-get -y install python-dev curl unzip && \
    cd /tmp && \
    curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" && \
    unzip awscli-bundle.zip && \
    ./awscli-bundle/install && \
    rm awscli-bundle.zip && \
    rm -rf awscli-bundle && \
    pip install --upgrade pip

# set up working directory
WORKDIR /prosperwooddesigns

# install all python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy all files, make image/log directories, and run app
COPY . .
RUN mkdir -p /prosperwooddesigns/app/static/images
CMD ["flask", "run"]
