# Standard library imports.
from typing import List, Optional

# Third party imports.
from ninja import NinjaAPI, Query

# Local imports.
from memories.models import Memory
from memories.schemas import MemoryCreateSchema, MemorySchema, NotFoundSchema

# Init the memories API.
api = NinjaAPI(urls_namespace="memories")


@api.get("/", response={200: MemorySchema, 404: NotFoundSchema})
def get_memory(request, namespace: List[str], key: str):
    try:
        return 200, Memory.objects.get(namespace=namespace, key=key)
    except Memory.DoesNotExist:
        return 404, {"message": "memory not found"}


@api.get("/search/", response=List[MemorySchema])
def search_memories(
    request,
    namespace_prefix: List[str] = Query(...),
    query: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    memories = Memory.objects.filter(namespace__0=namespace_prefix[0])
    return memories.order_by("-updated_at")[offset : offset + limit]


@api.post("/", response={201: MemoryCreateSchema})
def create_memory(request, payload: MemoryCreateSchema):
    memory, _ = Memory.objects.update_or_create(
        namespace=payload.namespace,
        key=payload.key,
        defaults={"value": payload.value},
    )
    return 201, memory


@api.delete("/", response={204: None, 404: NotFoundSchema})
def delete_memory(request, namespace: List[str], key: str):
    try:
        Memory.objects.get(namespace=namespace, key=key).delete()
        return 204, None
    except Memory.DoesNotExist:
        return 404, {"message": "memory not found"}
