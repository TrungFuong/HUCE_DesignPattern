from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.dashboard_service import DashboardService
from app.core.dependencies import get_current_user, get_db_session, get_mongo_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(
    db_session: AsyncSession = Depends(get_db_session),
    mongo_db=Depends(get_mongo_db),
) -> DashboardService:
    return DashboardService(mongo_db=mongo_db, db_session=db_session)


@router.get("/summary")
async def get_dashboard_summary(
    dashboard: DashboardService = Depends(get_dashboard_service),
    current_user: dict = Depends(get_current_user),
):
    """
    Tổng hợp dashboard: tổng số batch, số batch AT_RISK, sensor logs mới nhất.
    """
    return await dashboard.get_summary()


@router.get("/recent-sensors")
async def get_recent_sensors(
    limit: int = 20,
    dashboard: DashboardService = Depends(get_dashboard_service),
    current_user: dict = Depends(get_current_user),
):
    """
    Lấy danh sách sensor logs mới nhất từ tất cả các batch.
    """
    logs = await dashboard.get_recent_sensors(limit=limit)
    return {"sensor_logs": logs, "count": len(logs)}


@router.get("/batch-status")
async def get_batch_status_summary(
    dashboard: DashboardService = Depends(get_dashboard_service),
    current_user: dict = Depends(get_current_user),
):
    """
    Thống kê số batch theo trạng thái (CREATED, IN_TRANSIT, DELIVERED, AT_RISK...).
    """
    return await dashboard.get_batch_status_summary()
