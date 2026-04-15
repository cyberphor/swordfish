FROM alpine:3.23
LABEL image.authors="Vic Fernandez III <@cyberphor>"
ARG MCP_SERVER_ENDPOINT="http://swordfish-tools:8282/mcp"
ENV MCP_SERVER_ENDPOINT=${MCP_SERVER_ENDPOINT}
WORKDIR /home/swordfish/
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip uvicorn &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D swordfish -h /home/swordfish
COPY swordfish/ swordfish/
RUN chown -R swordfish:swordfish /home/swordfish
USER swordfish
EXPOSE 8181
ENTRYPOINT [ "uvicorn", "swordfish.main:api", "--host", "0.0.0.0", "--port", "8181" ]
