from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Index, Integer, String, UniqueConstraint, Unicode
from app.infrastructure.database.sqlserver.models import Base


class ShipmentModel(Base):
    __tablename__ = "shipments"
    __table_args__ = (
        CheckConstraint("end_time IS NULL OR end_time >= start_time", name="ck_shipments_end_after_start"),
        Index("ix_shipments_from_actor_id", "from_actor_id"),
        Index("ix_shipments_to_actor_id", "to_actor_id"),
        Index("ix_shipments_carrier_id", "carrier_id"),
    )

    id = Column(String(36), primary_key=True, index=True)
    from_actor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    to_actor_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    carrier_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    origin = Column(Unicode(255), nullable=False)
    destination = Column(Unicode(255), nullable=False)
    status = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    notes = Column(Unicode(500), nullable=True)


class ShipmentItemModel(Base):
    __tablename__ = "shipment_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_shipment_items_quantity_positive"),
        UniqueConstraint("shipment_id", "batch_id", "container_id", name="uq_shipment_items_manifest_line"),
        Index("ix_shipment_items_shipment_id", "shipment_id"),
        Index("ix_shipment_items_batch_id", "batch_id"),
        Index("ix_shipment_items_container_id", "container_id"),
    )

    id = Column(String(36), primary_key=True, index=True)
    shipment_id = Column(String(36), ForeignKey("shipments.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    container_id = Column(String(36), ForeignKey("containers.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    quantity_unit = Column(Unicode(20), nullable=False, default="kg")
