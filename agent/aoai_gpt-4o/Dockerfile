FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/swordfish/
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip uvicorn &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish
COPY entrypoint.sh entrypoint.sh
COPY swordfish/ swordfish/
RUN chown -R swordfish:swordfish /home/swordfish &&\
    chmod +x entrypoint.sh
USER swordfish
EXPOSE 8181
ENTRYPOINT [ "./entrypoint.sh" ]
