FROM nginx:1.27.0
RUN rm /var/log/nginx/*
COPY static/robots.txt /var/www/robots.txt
ARG NGINX_CONF
COPY $NGINX_CONF.default.conf /etc/nginx/conf.d/default.conf
