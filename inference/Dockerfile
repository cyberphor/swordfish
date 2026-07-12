FROM alpine:3.23
LABEL image.authors="Victor Fernandez III, @cyberphor"
WORKDIR /home/inference/
COPY swordfish/ swordfish/
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip uvicorn &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/inference/ &&\
    chown -R swordfish:swordfish /home/inference/
USER swordfish
EXPOSE 8001
CMD [ "uvicorn",  "swordfish.main:api", "--host", "0.0.0.0", "--port", "8001" ]
