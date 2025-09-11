FROM alpine:latest
LABEL image.authors="Victor Fernandez III, <@cyberphor>"
WORKDIR /home/narwhal
COPY . .
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt
CMD [ "python", "main.py" ]
