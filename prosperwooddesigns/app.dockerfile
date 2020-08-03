# app.dockerfile
# Michael Cole
#
# Dockerfile for the app's Python container
# -----------------------------------------

FROM python:3.7.5-slim
LABEL maintainer="Michael Cole <mcole042891.prof.dev@gmail.com>"

# install awscli
RUN apt-get update
RUN apt-get -y install python-dev curl unzip
RUN cd /tmp
RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
RUN unzip awscli-bundle.zip
RUN ./awscli-bundle/install
RUN rm awscli-bundle.zip
RUN rm -rf awscli-bundle

# set up working directory and images folder
WORKDIR /prosperwooddesigns
RUN TOUCH /prosperwooddesigns/app/static/images

# install all python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy all files and run app
COPY . .
CMD ["flask", "run"]
