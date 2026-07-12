FROM alpine:3.23
LABEL image.authors="Victor Fernandez III, <@cyberphor>"
WORKDIR /home/frontend/
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt
COPY .streamlit .streamlit
COPY swordfish/ swordfish/
RUN adduser -D swordfish -h /home/frontend/ &&\
    chown -R swordfish:swordfish /home/frontend/
USER swordfish
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "swordfish/main.py" ]
