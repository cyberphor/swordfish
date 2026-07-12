FROM alpine:3.23 AS stage_1
WORKDIR /home/tools/
RUN apk add --no-cache --update curl &&\
    curl -kL --output emu "https://github.com/deathlabs/emu/releases/download/v4.0.0/emu-linux-amd64" &&\
    chmod +x emu

FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/tools/
COPY --from=stage_1 /home/tools/emu /usr/local/bin/emu
COPY requirements.txt requirements.txt
COPY swordfish/ swordfish/
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/tools/ &&\
    chown -R swordfish:swordfish /home/tools/
USER swordfish
EXPOSE 8002
CMD [ "python", "-m", "swordfish.main" ]
