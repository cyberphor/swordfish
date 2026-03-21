FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY entrypoint.sh entrypoint.sh
COPY mkdocs.yml mkdocs.yml
COPY requirements.txt requirements.txt
COPY swordfish/ swordfish/
RUN apk add --no-cache --update mkdocs python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish &&\
    chmod +x entrypoint.sh
USER swordfish
EXPOSE 5050
ENTRYPOINT [ "./entrypoint.sh" ]
