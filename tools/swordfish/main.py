from os import environ
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP(name="swordfish", host="0.0.0.0", port=8282, debug=True, log_level="DEBUG")

EMASS_BASE_URL = environ.get("EMASS_BASE_URL", "")
EMASS_API_KEY = environ.get("EMASS_API_KEY", "")
EMASS_USER_UID = environ.get("EMASS_USER_UID", "")
SERPER_API_KEY = environ.get("SERPER_API_KEY", "")

def _headers() -> dict:
    return {
        "api-key": EMASS_API_KEY,
        "user-uid": EMASS_USER_UID,
        "accept": "application/json",
        "content-type": "application/json",
    }


def _get(path: str, params: dict = None) -> dict:
    url = f"{EMASS_BASE_URL}{path}"
    response = httpx.get(url, headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _post(path: str, body: list) -> dict:
    url = f"{EMASS_BASE_URL}{path}"
    response = httpx.post(url, headers=_headers(), json=body, timeout=30)
    response.raise_for_status()
    return response.json()


def _put(path: str, body: list) -> dict:
    url = f"{EMASS_BASE_URL}{path}"
    response = httpx.put(url, headers=_headers(), json=body, timeout=30)
    response.raise_for_status()
    return response.json()


def _delete(path: str, body: list) -> dict:
    url = f"{EMASS_BASE_URL}{path}"
    response = httpx.request("DELETE", url, headers=_headers(), json=body, timeout=30)
    response.raise_for_status()
    return response.json()

@mcp.tool(description="Test the connection to the eMASS API.")
def test_connection() -> dict:
    return _get("/api")

# Systems

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

# Controls

@mcp.tool(description="Get security controls for a system. Optionally filter by control acronyms (comma-separated, e.g. 'AC-1,AC-2').")
def get_controls(system_id: int, acronyms: str = None) -> dict:
    params = {}
    if acronyms:
        params["acronyms"] = acronyms
    return _get(f"/api/systems/{system_id}/controls", params=params)


@mcp.tool(description=(
    "Update one or more security controls for a system. "
    "Each item requires: acronym, responsibleEntities, controlDesignation, "
    "estimatedCompletionDate (epoch int), implementationNarrative. "
    "Pass a list of control objects as `controls`."
))
def update_controls(system_id: int, controls: list[dict]) -> dict:
    return _put(f"/api/systems/{system_id}/controls", controls)

# Test Results

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


@mcp.tool(description=(
    "Add one or more test results to a system. "
    "Each item requires: testedBy (str), testDate (epoch int), description (str), "
    "complianceStatus (str), assessmentProcedure (str). "
    "Pass a list of test result objects as `results`."
))
def add_test_results(system_id: int, results: list[dict]) -> dict:
    return _post(f"/api/systems/{system_id}/test-results", results)

# POA&Ms

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


@mcp.tool(description=(
    "Add one or more POA&M items to a system. "
    "Each item requires: status, vulnerabilityDescription, sourceIdentifyingVulnerability, "
    "pocOrganization, resources. "
    "Conditional fields (include when applicable): scheduledCompletionDate (epoch int), "
    "completionDate (epoch int), comments, severity, pocFirstName, pocLastName, "
    "pocEmail, pocPhoneNumber. "
    "Pass a list of POA&M objects as `poams`."
))
def add_poams(system_id: int, poams: list[dict]) -> dict:
    return _post(f"/api/systems/{system_id}/poams", poams)


@mcp.tool(description=(
    "Update one or more existing POA&M items in a system. "
    "Each item requires: poamId, displayPoamId, status, vulnerabilityDescription, "
    "sourceIdentifyingVulnerability, pocOrganization, resources. "
    "Pass a list of POA&M objects as `poams`."
))
def update_poams(system_id: int, poams: list[dict]) -> dict:
    return _put(f"/api/systems/{system_id}/poams", poams)


@mcp.tool(description=(
    "Delete one or more POA&M items from a system. "
    "Pass a list of objects each containing a single `poamId` (int) as `poam_ids`. "
    "Example: [{'poamId': 45}, {'poamId': 46}]"
))
def delete_poams(system_id: int, poam_ids: list[dict]) -> dict:
    return _delete(f"/api/systems/{system_id}/poams", poam_ids)

def _serper_search(query: str, num_results: int = 10) -> dict:
    response = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY, "content-type": "application/json"},
        json={"q": query, "num": num_results},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

@mcp.tool(description="Search the web using Google (via Serper). Returns organic results, knowledge graph, and answer box when available.")
def web_search(query: str, num_results: int = 10) -> dict:
    return _serper_search(query, num_results)

if __name__ == "__main__":
    mcp.run(transport="sse")