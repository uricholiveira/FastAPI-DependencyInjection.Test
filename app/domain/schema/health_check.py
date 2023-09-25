from pydantic import BaseModel


class HealthCheckAppResponse(BaseModel):
    name: str
    status: str
    version: str


class HealthCheckDatabaseResponse(BaseModel):
    is_active: bool


class HealthCheckDiskResponse(BaseModel):
    free: float
    used: float
    total: float
    percent: float


class HealthCheckCPUResponse(BaseModel):
    percent: float


class HealthCheckMemoryResponse(BaseModel):
    total: float
    available: float
    percent: float


class HealthCheckResponse(BaseModel):
    service: HealthCheckAppResponse
    cpu: HealthCheckCPUResponse
    disk: HealthCheckDiskResponse
    database: HealthCheckDatabaseResponse
    memory: HealthCheckMemoryResponse
