FROM nginx:1.27.0
ENV CONF_FILE=http NUM_WORKERS=20
RUN rm /var/log/nginx/*
COPY ${CONF_FILE}.conf /etc/nginx/conf.d/default.conf
COPY static/robots.txt /var/www/robots.txt
