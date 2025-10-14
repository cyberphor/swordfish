FROM alpine:3.22 AS stage_1
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
RUN apk add --no-cache --update curl nodejs npm &&\
    npm install -g @stoplight/prism-cli &&\
    curl -o eMASSRestOpenApi.yaml https://raw.githubusercontent.com/mitre/emass_client/refs/heads/main/docs/eMASSRestOpenApi.yaml &&\
    apk del curl &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish
USER swordfish
CMD [ "prism", "mock", "eMASSRestOpenApi.yaml", "--host", "0.0.0.0", "--port", "4010" ]
