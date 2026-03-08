FROM alpine:latest
LABEL image.authors="Victor Fernandez III, <@cyberphor>"
WORKDIR /home/swordfish
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt
EXPOSE 8501
CMD [ "streamlit", "run", "main.py" ]
