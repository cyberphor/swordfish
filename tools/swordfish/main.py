# Standard library imports.
from os import environ, unlink
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request
import base64
import json

# Third party imports.
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentHeaders

EMASS_API_URL = environ["EMASS_API_URL"]
DOD_CERTS_PATH = environ["DOD_CERTS_PATH"]

mcp = FastMCP(name="swordfish")

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

def _get_headers(headers: dict[str, str], name: str) -> str:
    value = headers.get(name)
    if not value:
        raise ValueError(f"missing required header: {name}")
    return value

def _get(path: str, headers: dict[str, str]) -> dict:
    api_key = _get_headers(headers, "x-emass-api-key")
    user_uid = _get_headers(headers, "x-emass-user-uid")
    public_cert_pem = base64.b64decode( _get_headers(headers, "x-emass-public-cert"))
    private_key_pem = base64.b64decode(_get_headers(headers, "x-emass-private-key"))
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
    with urlopen(request, context=ctx, timeout=120) as response:
        return json.loads(response.read())

@mcp.tool(description="Test connectivity to eMASS.")
def test_connection(headers: dict[str, str] = CurrentHeaders()) -> dict:
    return _get("/api", headers)

@mcp.tool(description="Get details for a specific eMASS system by its system ID.")
def get_system(system_id: int, headers: dict[str, str] = CurrentHeaders()) -> dict:
    return _get(f"/api/systems/{system_id}", headers)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8282,
    )
