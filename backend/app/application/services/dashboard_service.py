from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.sqlserver.repositories.sql_batch_repository import SqlBatchRepository


class DashboardService:
    """Tổng hợp số liệu cho dashboard — đọc từ MongoDB (sensor logs) và SQL Server (batches)."""

    def __init__(self, mongo_db: AsyncIOMotorDatabase, db_session: AsyncSession):
        self.mongo_db = mongo_db
        self.db_session = db_session

    async def get_summary(self) -> dict:
        """Trả về tổng hợp: batch counts, at-risk count, recent sensor readings."""
        batch_service = SqlBatchRepository(self.db_session)
        batches = await batch_service.find_all()

        total_batches = len(batches)
        at_risk_count = sum(
            1 for b in batches if getattr(b, "status", None) is not None
            and str(getattr(b, "status", "")).upper() == "AT_RISK"
        )

        recent_logs = await self._get_recent_sensor_logs(limit=20)

        return {
            "total_batches": total_batches,
            "at_risk_batches": at_risk_count,
            "normal_batches": total_batches - at_risk_count,
            "recent_sensor_logs": recent_logs,
            "generated_at": datetime.utcnow().isoformat(),
        }

    async def get_recent_sensors(self, limit: int = 20) -> list[dict]:
        """Lấy sensor logs mới nhất từ toàn bộ batches."""
        return await self._get_recent_sensor_logs(limit=limit)

    async def get_batch_status_summary(self) -> list[dict]:
        """Thống kê số batch theo từng trạng thái."""
        batch_service = SqlBatchRepository(self.db_session)
        batches = await batch_service.find_all()

        status_counts: dict[str, int] = {}
        for batch in batches:
            status_key = str(getattr(batch, "status", "UNKNOWN")).upper()
            status_counts[status_key] = status_counts.get(status_key, 0) + 1

        return [{"status": k, "count": v} for k, v in status_counts.items()]

    async def _get_recent_sensor_logs(self, limit: int = 20) -> list[dict]:
        """Truy vấn MongoDB lấy sensor_logs mới nhất."""
        try:
            collection = self.mongo_db["sensor_logs"]
            cursor = collection.find({}).sort("recorded_at", -1).limit(limit)
            docs = await cursor.to_list(length=limit)
            result = []
            for doc in docs:
                doc.pop("_id", None)
                if hasattr(doc.get("recorded_at"), "isoformat"):
                    doc["recorded_at"] = doc["recorded_at"].isoformat()
                result.append(doc)
            return result
        except Exception:
            return []
