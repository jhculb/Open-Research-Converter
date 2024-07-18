FROM node:latest
COPY orc-demo/ /orc-demo/
WORKDIR /orc-demo/
RUN npm install
ENTRYPOINT [ "npm", "start" ]