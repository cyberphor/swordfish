FROM alpine:3.23
LABEL image.authors="Victor Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY mkdocs.yml mkdocs.yml
COPY swordfish/ swordfish/
RUN apk add --no-cache --update mkdocs python3 py3-pip &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish &&\
USER swordfish
EXPOSE 5050
CMD [ "mkdocs", "serve", "--dev-addr=0.0.0.0:5050" ]
