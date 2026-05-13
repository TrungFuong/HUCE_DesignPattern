from pydantic import BaseModel


class BlockchainVerificationResponse(BaseModel):
    batch_id: str
    current_hash: str
    blockchain_hash: str | None
    is_valid: bool
