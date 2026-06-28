from pydantic import BaseModel


class CropTypeRequest(BaseModel):
    code: str
    name: str
    description: str | None = None


class CropTypeResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str | None = None
