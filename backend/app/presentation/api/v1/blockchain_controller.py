from fastapi import APIRouter, Depends, HTTPException

from app.application.services.blockchain_service import BlockchainService
from app.core.dependencies import get_blockchain_service, require_roles
from app.domain.enums.role import RoleName

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


@router.get("/verify/{batch_id}")
async def verify_batch_hash(
    batch_id: str,
    blockchain_service: BlockchainService = Depends(get_blockchain_service),
    current_user: dict = Depends(require_roles(RoleName.ADMIN)),
):
    """
    Lấy hash đang lưu trên blockchain cho batch_id.
    Dùng để xác minh tính toàn vẹn của dữ liệu OCOP.
    """
    stored_hash = await blockchain_service.get_hash(batch_id)
    if stored_hash is None:
        raise HTTPException(status_code=404, detail=f"No blockchain record found for batch_id={batch_id}")
    return {
        "batch_id": batch_id,
        "blockchain_hash": stored_hash,
        "is_verified": bool(stored_hash),
    }


@router.get("/hash/{batch_id}")
async def get_batch_hash(
    batch_id: str,
    blockchain_service: BlockchainService = Depends(get_blockchain_service),
):
    """
    Endpoint công khai: lấy hash từ blockchain (không cần auth).
    Dành cho người dùng quét QR muốn xác minh nguồn gốc.
    """
    stored_hash = await blockchain_service.get_hash(batch_id)
    return {
        "batch_id": batch_id,
        "blockchain_hash": stored_hash,
        "verified": stored_hash is not None and len(stored_hash) > 0,
    }
