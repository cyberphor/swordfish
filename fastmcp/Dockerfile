FROM alpine:3.23 AS stage_1
WORKDIR /home/swordfish/
RUN apk add --no-cache --update curl &&\
    curl -kL --output emu "https://github.com/deathlabs/emu/releases/download/v4.0.0/emu-linux-amd64" &&\
    chmod +x emu

FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY --from=stage_1 /home/swordfish/emu /usr/local/bin/emu
COPY requirements.txt requirements.txt
COPY swordfish/ swordfish/
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish
USER swordfish
EXPOSE 8282
CMD [ "python", "-m", "swordfish.main" ]
