# Standard library imports.
from base64 import b64decode
from logging import DEBUG, getLogger
from logging.config import dictConfig
from os import environ, path
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request

# Third party imports.
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentHeaders

# Configure the FastMCP server's log settings.
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "handlers": ["default"],
            "level": "INFO",
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "propagate": False},
            "uvicorn.error": {"handlers": ["default"], "propagate": False},
            "uvicorn.access": {"handlers": ["default"], "propagate": False},
        },
    }
)
logger = getLogger(__name__)

# Set and check environment variables.
EMASS_API_URL = environ["EMASS_API_URL"]
DOD_CERTS_PATH = environ["DOD_CERTS_PATH"]
if not path.exists(DOD_CERTS_PATH):
    raise RuntimeError(f"DOD_CERTS_PATH not found: {DOD_CERTS_PATH}")

# Init a FastMCP server.
mcp = FastMCP(name="swordfish")


# Builds SSL context for HTTPS requests made by the FastMCP server.
def _build_ssl_context(public_cert_pem: bytes, private_key_pem: bytes) -> SSLContext:
    ctx = SSLContext(PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(DOD_CERTS_PATH)
    with (
        NamedTemporaryFile("wb", delete=False, suffix=".pem") as cert_file,
        NamedTemporaryFile("wb", delete=False, suffix=".pem") as key_file,
    ):
        cert_file.write(public_cert_pem)
        cert_file.flush()
        cert_path = cert_file.name
        key_file.write(private_key_pem)
        key_file.flush()
        key_path = key_file.name
        ctx.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return ctx


# Parses HTTP headers by name.
def _get_headers(headers: dict[str, str], name: str) -> str:
    value = headers.get(name)
    if not value:
        raise ValueError(f"missing required header: {name}")
    return value


# Sends an HTTP GET request to eMASS.
def _emass_get_request(path: str, headers: dict[str, str]) -> dict:
    api_key = _get_headers(headers, "x-emass-api-key")
    user_uid = _get_headers(headers, "x-emass-user-uid")
    public_cert_pem = b64decode(_get_headers(headers, "x-emass-public-cert"))
    private_key_pem = b64decode(_get_headers(headers, "x-emass-private-key"))
    ctx = _build_ssl_context(public_cert_pem, private_key_pem)
    request = Request(
        url=f"{EMASS_API_URL}{path}",
        headers={
            "api-key": api_key,
            "user-uid": user_uid,
            "accept": "application/json",
            "content-type": "application/json",
        },
    )
    with urlopen(request, context=ctx, timeout=240) as response:
        output = response.read().decode("UTF-8")
        print(output)
        return output


@mcp.tool(description="Test connectivity to eMASS.")
def test_connection(
    headers: dict[str, str] = CurrentHeaders(),
) -> dict:
    response = _emass_get_request("/api", headers)
    logger.log(level=DEBUG, msg=response)
    return response


@mcp.tool(description="Get details for a specific eMASS system by its system ID.")
def get_system(system_id: int, headers: dict[str, str] = CurrentHeaders()) -> dict:
    response = _emass_get_request(f"/api/systems/{system_id}", headers)
    logger.log(level=DEBUG, msg=response)
    return response


@mcp.tool(description="Get information about a specific system's artifacts in eMASS.")
def get_artifacts(system_id: int, headers: dict[str, str] = CurrentHeaders()) -> list:
    api_key = _get_headers(headers, "x-emass-api-key")
    user_uid = _get_headers(headers, "x-emass-user-uid")
    public_cert_pem = b64decode(_get_headers(headers, "x-emass-public-cert"))
    private_key_pem = b64decode(_get_headers(headers, "x-emass-private-key"))
    with (
        NamedTemporaryFile("wb", delete=False, suffix=".pem") as cert_file,
        NamedTemporaryFile("wb", delete=False, suffix=".pem") as key_file,
        NamedTemporaryFile("w", delete=False, suffix=".yaml") as config_file,
    ):
        cert_file.write(public_cert_pem)
        cert_file.flush()
        key_file.write(private_key_pem)
        key_file.flush()
        config_file.write(f"""---
url: {EMASS_API_URL}
profiles:
  - name: default
    publicKeyPath: {cert_file.name}
    privateKeyPath: {key_file.name}
systems:
  - name: target
    id: {system_id}
    profile: default
settings:
  output:
    format: json
""")
        config_file.flush()
        env = environ.copy()
        env["EMASS_USER_UID_DEFAULT"] = user_uid
        env["EMASS_API_KEY_DEFAULT"] = api_key
        process = Popen(
            [
                "emu",
                "get",
                "artifacts",
                "--system-id",
                str(system_id),
                "--config",
                config_file.name,
            ],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            env=env,
        )
        output, errors = process.communicate(timeout=300)
    if process.returncode != 0:
        raise RuntimeError(f"emu failed: {errors}")
    print(output)
    return output


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8282,
    )
