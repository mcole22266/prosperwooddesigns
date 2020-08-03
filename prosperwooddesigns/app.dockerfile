# app.dockerfile
# Michael Cole
#
# Dockerfile for the app's Python container
# -----------------------------------------

FROM python:3.7.5-slim
LABEL maintainer="Michael Cole <mcole042891.prof.dev@gmail.com>"

WORKDIR /prosperwooddesigns

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]
