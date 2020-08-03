# nginx.dockerfile
# Michael Cole
#
# Dockerfile for the production server container
# ----------------------------------------------

FROM nginx:1.17-alpine
LABEL maintainer="Michael Cole <mcole042891.prof.dev@gmail.com>"

# replace default configuration file with custom
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
