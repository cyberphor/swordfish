FROM alpine:3.22 AS stage_1
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY swordfish/ swordfish/
COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish &&\
    chmod +x entrypoint.sh
USER swordfish
ENTRYPOINT [ "./entrypoint.sh" ]
