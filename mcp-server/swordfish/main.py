# mcp/main.py
from os import environ
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP(name="swordfish", host="0.0.0.0", port=8282, debug=True, log_level="DEBUG")

EMASS_BASE_URL = environ.get("EMASS_BASE_URL", "https://stoplight.io/mocks/mitre/emasser/32836028")
EMASS_API_KEY = environ.get("EMASS_API_KEY", "")
EMASS_USER_UID = environ.get("EMASS_USER_UID", "")

def _headers() -> dict:
    return {
        "api-key": EMASS_API_KEY,
        "user-uid": EMASS_USER_UID,
        "accept": "application/json",
    }

def _get(path: str, params: dict = None) -> dict:
    url = f"{EMASS_BASE_URL}{path}"
    response = httpx.get(url, headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


@mcp.tool(description="Test the connection to the eMASS API.")
def test_connection() -> dict:
    return _get("/api")


@mcp.tool(description="Get a list of all systems the user has access to in eMASS.")
def get_systems(
    include_decommissioned: bool = False,
    policy: str = None,
) -> dict:
    params = {"includeDecommissioned": include_decommissioned}
    if policy:
        params["policy"] = policy
    return _get("/api/systems", params=params)


@mcp.tool(description="Get details for a specific eMASS system by its system ID.")
def get_system(system_id: int) -> dict:
    return _get(f"/api/systems/{system_id}")


@mcp.tool(description="Get security controls for a system. Optionally filter by control acronyms (comma-separated, e.g. 'AC-1,AC-2').")
def get_controls(system_id: int, acronyms: str = None) -> dict:
    params = {}
    if acronyms:
        params["acronyms"] = acronyms
    return _get(f"/api/systems/{system_id}/controls", params=params)


@mcp.tool(description="Get POA&M items for a system. Optionally filter by control acronyms or date range (epoch seconds).")
def get_poams(
    system_id: int,
    control_acronyms: str = None,
    scheduled_completion_date_start: int = None,
    scheduled_completion_date_end: int = None,
) -> dict:
    params = {}
    if control_acronyms:
        params["controlAcronyms"] = control_acronyms
    if scheduled_completion_date_start:
        params["scheduledCompletionDateStart"] = scheduled_completion_date_start
    if scheduled_completion_date_end:
        params["scheduledCompletionDateEnd"] = scheduled_completion_date_end
    return _get(f"/api/systems/{system_id}/poams", params=params)


@mcp.tool(description="Get test results for a system. Optionally filter by control acronyms or CCIs.")
def get_test_results(
    system_id: int,
    control_acronyms: str = None,
    ccis: str = None,
    latest_only: bool = True,
) -> dict:
    params = {"latestOnly": latest_only}
    if control_acronyms:
        params["controlAcronyms"] = control_acronyms
    if ccis:
        params["ccis"] = ccis
    return _get(f"/api/systems/{system_id}/test-results", params=params)


if __name__ == "__main__":
    mcp.run(transport="sse")