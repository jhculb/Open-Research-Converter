ARG NODE_VERSION=22.9.0
FROM node:${NODE_VERSION}
WORKDIR /orc-demo/
COPY orc-demo/package.json orc-demo/package-lock.json /orc-demo/
RUN npm install
COPY orc-demo/public/ /orc-demo/public
COPY orc-demo/src /orc-demo/src
ENTRYPOINT [ "npm", "start" ]
