ARG NGINX_VERSION=1.27.0
FROM nginx:${NGINX_VERSION}
RUN rm /var/log/nginx/*
COPY static/  /var/nginx/www/
ARG NGINX_CONF
COPY $NGINX_CONF.default.conf /etc/nginx/conf.d/default.conf
