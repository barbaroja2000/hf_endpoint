from pydantic import BaseModel, Field
from typing import Dict, Any

class CustomImage(BaseModel):
    url: str
    health_route: str
    env: Dict[str, str]

class Model(BaseModel):
    repository: str
    revision: str
    task: str
    framework: str
    image: Dict[str, CustomImage]

class Scaling(BaseModel):
    minReplica: int
    maxReplica: int

class Compute(BaseModel):
    accelerator: str
    instanceSize: str
    instanceType: str
    scaling: Scaling

class Provider(BaseModel):
    region: str
    vendor: str

class EndpointPayload(BaseModel):
    accountId: Any = Field(None)
    compute: Compute
    model: Model
    name: str
    provider: Provider
    type: str