FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY entrypoint.sh entrypoint.sh
COPY swordfish/ swordfish/
COPY requirements.txt requirements.txt
COPY smollm2-360m-instruct-q8_0.gguf smollm2-360m-instruct-q8_0.gguf
RUN apk add --no-cache --update build-base cmake python3 py3-pip uvicorn &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish &&\
    chown -R swordfish:swordfish /home/swordfish &&\
    chmod +x entrypoint.sh
USER swordfish
EXPOSE 8181
ENTRYPOINT [ "./entrypoint.sh" ]
