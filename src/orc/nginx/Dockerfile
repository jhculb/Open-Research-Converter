FROM nginx:1.27.0
RUN rm /var/log/nginx/*
COPY static/robots.txt /var/www/robots.txt
ENV CONF_FILE=https
COPY ${CONF_FILE}.conf /etc/nginx/conf.d/default.conf
