"""
Seed data cho hệ thống OCOP Traceability.
Chạy tự động khi startup — chỉ seed nếu DB chưa có data.
"""

import logging
import uuid
from datetime import datetime, timedelta

from app.core.security import hash_password
from app.domain.enums.role import RoleName

logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━ Cố định ID để các bảng liên kết được ━━━━━━━━━━━━━━━━

# Users
ADMIN_ID = "00000000-0000-0000-0000-000000000001"
FARMER_1_ID = "00000000-0000-0000-0000-000000000002"
FARMER_2_ID = "00000000-0000-0000-0000-000000000003"
TRADER_ID = "00000000-0000-0000-0000-000000000004"
DISTRIBUTOR_ID = "00000000-0000-0000-0000-000000000005"

# Farms
FARM_1_ID = "10000000-0000-0000-0000-000000000001"
FARM_2_ID = "10000000-0000-0000-0000-000000000002"
FARM_3_ID = "10000000-0000-0000-0000-000000000003"

# CropTypes
CT_LUA_ID = "20000000-0000-0000-0000-000000000001"
CT_CAPHE_ID = "20000000-0000-0000-0000-000000000002"
CT_TIEU_ID = "20000000-0000-0000-0000-000000000003"
CT_CHANHDAY_ID = "20000000-0000-0000-0000-000000000004"

# Chemicals
CHEM_LUA_1 = "30000000-0000-0000-0000-000000000001"
CHEM_LUA_2 = "30000000-0000-0000-0000-000000000002"
CHEM_LUA_3 = "30000000-0000-0000-0000-000000000003"
CHEM_CAPHE_1 = "30000000-0000-0000-0000-000000000004"
CHEM_CAPHE_2 = "30000000-0000-0000-0000-000000000005"
CHEM_TIEU_1 = "30000000-0000-0000-0000-000000000006"
CHEM_TIEU_2 = "30000000-0000-0000-0000-000000000007"
CHEM_CHANHDAY_1 = "30000000-0000-0000-0000-000000000008"

# Batches
BATCH_1_ID = "40000000-0000-0000-0000-000000000001"
BATCH_2_ID = "40000000-0000-0000-0000-000000000002"
BATCH_3_ID = "40000000-0000-0000-0000-000000000003"
BATCH_4_ID = "40000000-0000-0000-0000-000000000004"
BATCH_5_ID = "40000000-0000-0000-0000-000000000005"

# Containers
CONT_1_ID = "50000000-0000-0000-0000-000000000001"
CONT_2_ID = "50000000-0000-0000-0000-000000000002"
CONT_3_ID = "50000000-0000-0000-0000-000000000003"

# Risk Rules
RR_LUA_ID = "60000000-0000-0000-0000-000000000001"
RR_CAPHE_ID = "60000000-0000-0000-0000-000000000002"
RR_TIEU_ID = "60000000-0000-0000-0000-000000000003"
RR_CHANHDAY_ID = "60000000-0000-0000-0000-000000000004"

NOW = datetime.utcnow()


async def seed_all(session) -> None:
    """Seed toàn bộ dữ liệu mẫu. Bỏ qua nếu đã có user farmer1."""
    from app.infrastructure.database.sqlserver.models.user_model import UserModel
    from app.infrastructure.database.sqlserver.models.farm_model import FarmModel
    from app.infrastructure.database.sqlserver.models.crop_type_model import CropTypeModel
    from app.infrastructure.database.sqlserver.models.chemical_model import ChemicalModel
    from app.infrastructure.database.sqlserver.models.batch_model import BatchModel
    from app.infrastructure.database.sqlserver.models.batch_chemical_model import BatchChemicalModel
    from app.infrastructure.database.sqlserver.models.container_model import ContainerModel
    from app.infrastructure.database.sqlserver.models.risk_rule_model import RiskRuleModel

    # Kiểm tra xem đã seed chưa
    existing = await session.get(UserModel, FARMER_1_ID)
    if existing:
        logger.info("[Seed] Dữ liệu mẫu đã tồn tại, bỏ qua.")
        return

    logger.info("[Seed] Bắt đầu seed dữ liệu mẫu...")

    # ──────────────── 1. USERS ────────────────
    password = hash_password("Abc@1234")
    users = [
        UserModel(id=FARMER_1_ID, full_name="Nguyễn Văn An", email="farmer1@ocop.vn",
                  password_hash=password, role=int(RoleName.FARMER), is_active=True, created_at=NOW),
        UserModel(id=FARMER_2_ID, full_name="Trần Thị Bình", email="farmer2@ocop.vn",
                  password_hash=password, role=int(RoleName.FARMER), is_active=True, created_at=NOW),
        UserModel(id=TRADER_ID, full_name="Lê Minh Cường", email="trader@ocop.vn",
                  password_hash=password, role=int(RoleName.TRADER), is_active=True, created_at=NOW),
        UserModel(id=DISTRIBUTOR_ID, full_name="Phạm Đức Duy", email="distributor@ocop.vn",
                  password_hash=password, role=int(RoleName.DISTRIBUTOR), is_active=True, created_at=NOW),
    ]
    session.add_all(users)
    await session.flush()

    # ──────────────── 2. FARMS ────────────────
    farms = [
        FarmModel(id=FARM_1_ID, owner_id=FARMER_1_ID, name="Nông trại Lúa Hữu Cơ An Giang",
                  address="Xã Thoại Sơn, An Giang",
                  planting_date=NOW - timedelta(days=120), harvest_date=NOW - timedelta(days=10)),
        FarmModel(id=FARM_2_ID, owner_id=FARMER_1_ID, name="Nông trại Cà Phê Đắk Lắk",
                  address="Xã Ea Tul, Cư M'gar, Đắk Lắk",
                  planting_date=NOW - timedelta(days=365), harvest_date=NOW - timedelta(days=30)),
        FarmModel(id=FARM_3_ID, owner_id=FARMER_2_ID, name="Nông trại Tiêu Phú Quốc",
                  address="Xã Cửa Dương, Phú Quốc, Kiên Giang",
                  planting_date=NOW - timedelta(days=240), harvest_date=NOW - timedelta(days=5)),
    ]
    session.add_all(farms)
    await session.flush()

    # ──────────────── 3. CROP TYPES ────────────────
    crop_types = [
        CropTypeModel(id=CT_LUA_ID, code="LUA", name="Lúa", description="Lúa nước, lúa gạo các loại"),
        CropTypeModel(id=CT_CAPHE_ID, code="CAPHE", name="Cà Phê", description="Cà phê Robusta & Arabica"),
        CropTypeModel(id=CT_TIEU_ID, code="TIEU", name="Hồ Tiêu", description="Tiêu đen, tiêu trắng, tiêu đỏ"),
        CropTypeModel(id=CT_CHANHDAY_ID, code="CHANHDAY", name="Chanh Dây", description="Chanh dây tím Lâm Đồng"),
    ]
    session.add_all(crop_types)
    await session.flush()

    # ──────────────── 4. CHEMICALS ────────────────
    chemicals = [
        # Hóa chất cho Lúa
        ChemicalModel(id=CHEM_LUA_1, crop_type_id=CT_LUA_ID,
                      name="Đạm Urê", unit="kg", description="Phân đạm urê CO(NH₂)₂ — bón thúc cho lúa"),
        ChemicalModel(id=CHEM_LUA_2, crop_type_id=CT_LUA_ID,
                      name="Thuốc trừ sâu Regent", unit="ml", description="Thuốc trừ sâu cuốn lá, rầy nâu"),
        ChemicalModel(id=CHEM_LUA_3, crop_type_id=CT_LUA_ID,
                      name="Phân Kali (KCl)", unit="kg", description="Bón lót giúp hạt chắc, tăng năng suất"),
        # Hóa chất cho Cà Phê
        ChemicalModel(id=CHEM_CAPHE_1, crop_type_id=CT_CAPHE_ID,
                      name="NPK 16-16-8", unit="kg", description="Phân bón tổng hợp cho cà phê"),
        ChemicalModel(id=CHEM_CAPHE_2, crop_type_id=CT_CAPHE_ID,
                      name="Thuốc trừ bệnh Anvil 5SC", unit="ml", description="Trị bệnh gỉ sắt lá cà phê"),
        # Hóa chất cho Hồ Tiêu
        ChemicalModel(id=CHEM_TIEU_1, crop_type_id=CT_TIEU_ID,
                      name="Phân hữu cơ vi sinh", unit="kg", description="Cải tạo đất, tăng vi sinh vật có lợi"),
        ChemicalModel(id=CHEM_TIEU_2, crop_type_id=CT_TIEU_ID,
                      name="Thuốc trừ nấm Ridomil Gold", unit="g", description="Phòng trị bệnh chết nhanh chết chậm"),
        # Hóa chất cho Chanh Dây
        ChemicalModel(id=CHEM_CHANHDAY_1, crop_type_id=CT_CHANHDAY_ID,
                      name="Canxi Bo", unit="ml", description="Bổ sung canxi, bo chống rụng hoa trái"),
    ]
    session.add_all(chemicals)
    await session.flush()

    # ──────────────── 5. BATCHES ────────────────
    batches = [
        BatchModel(id=BATCH_1_ID, farm_id=FARM_1_ID, crop_type_id=CT_LUA_ID,
                   product_name="Gạo ST25 Hữu Cơ", harvest_date=NOW - timedelta(days=10),
                   quantity=500, quantity_unit="kg", grade="OCOP 4 sao",
                   status=0, risk_level=0),
        BatchModel(id=BATCH_2_ID, farm_id=FARM_1_ID, crop_type_id=CT_LUA_ID,
                   product_name="Gạo Jasmine", harvest_date=NOW - timedelta(days=8),
                   quantity=300, quantity_unit="kg", grade="OCOP 3 sao",
                   status=0, risk_level=0),
        BatchModel(id=BATCH_3_ID, farm_id=FARM_2_ID, crop_type_id=CT_CAPHE_ID,
                   product_name="Cà Phê Robusta Đắk Lắk", harvest_date=NOW - timedelta(days=30),
                   quantity=200, quantity_unit="kg", grade="OCOP 5 sao",
                   status=1, risk_level=0),
        BatchModel(id=BATCH_4_ID, farm_id=FARM_3_ID, crop_type_id=CT_TIEU_ID,
                   product_name="Tiêu Đen Phú Quốc", harvest_date=NOW - timedelta(days=5),
                   quantity=100, quantity_unit="kg", grade="OCOP 4 sao",
                   status=0, risk_level=0),
        BatchModel(id=BATCH_5_ID, farm_id=FARM_3_ID, crop_type_id=CT_CHANHDAY_ID,
                   product_name="Chanh Dây Tím Lâm Đồng", harvest_date=NOW - timedelta(days=3),
                   quantity=150, quantity_unit="kg", grade="OCOP 3 sao",
                   status=0, risk_level=0),
    ]
    session.add_all(batches)
    await session.flush()

    # ──────────────── 6. BATCH CHEMICALS ────────────────
    batch_chemicals = [
        # Batch 1 (Gạo ST25) dùng 2 hóa chất
        BatchChemicalModel(batch_id=BATCH_1_ID, chemical_id=CHEM_LUA_1,
                           applied_at=NOW - timedelta(days=60), is_deleted=False),
        BatchChemicalModel(batch_id=BATCH_1_ID, chemical_id=CHEM_LUA_3,
                           applied_at=NOW - timedelta(days=30), is_deleted=False),
        # Batch 2 (Gạo Jasmine) dùng 3 hóa chất
        BatchChemicalModel(batch_id=BATCH_2_ID, chemical_id=CHEM_LUA_1,
                           applied_at=NOW - timedelta(days=50), is_deleted=False),
        BatchChemicalModel(batch_id=BATCH_2_ID, chemical_id=CHEM_LUA_2,
                           applied_at=NOW - timedelta(days=40), is_deleted=False),
        BatchChemicalModel(batch_id=BATCH_2_ID, chemical_id=CHEM_LUA_3,
                           applied_at=NOW - timedelta(days=20), is_deleted=False),
        # Batch 3 (Cà Phê Robusta) dùng 2 hóa chất
        BatchChemicalModel(batch_id=BATCH_3_ID, chemical_id=CHEM_CAPHE_1,
                           applied_at=NOW - timedelta(days=90), is_deleted=False),
        BatchChemicalModel(batch_id=BATCH_3_ID, chemical_id=CHEM_CAPHE_2,
                           applied_at=NOW - timedelta(days=60), is_deleted=False),
        # Batch 4 (Tiêu Đen) dùng 1 hóa chất
        BatchChemicalModel(batch_id=BATCH_4_ID, chemical_id=CHEM_TIEU_1,
                           applied_at=NOW - timedelta(days=45), is_deleted=False),
        # Batch 5 (Chanh Dây) dùng 1 hóa chất
        BatchChemicalModel(batch_id=BATCH_5_ID, chemical_id=CHEM_CHANHDAY_1,
                           applied_at=NOW - timedelta(days=15), is_deleted=False),
    ]
    session.add_all(batch_chemicals)

    # ──────────────── 7. CONTAINERS ────────────────
    containers = [
        ContainerModel(id=CONT_1_ID, code="CONT-LANH-001", type="Container lạnh",
                       capacity=5000, capacity_unit="kg", material="Thép không gỉ",
                       is_temperature_controlled=True, min_temperature=2.0, max_temperature=8.0,
                       status=0, description="Container lạnh vận chuyển nông sản tươi"),
        ContainerModel(id=CONT_2_ID, code="CONT-KHO-001", type="Container khô",
                       capacity=10000, capacity_unit="kg", material="Thép",
                       is_temperature_controlled=False, min_temperature=None, max_temperature=None,
                       status=0, description="Container khô vận chuyển gạo, cà phê"),
        ContainerModel(id=CONT_3_ID, code="CONT-LANH-002", type="Container lạnh mini",
                       capacity=2000, capacity_unit="kg", material="Nhôm hợp kim",
                       is_temperature_controlled=True, min_temperature=0.0, max_temperature=5.0,
                       status=1, description="Container nhỏ cho vận chuyển nội tỉnh"),
    ]
    session.add_all(containers)

    # ──────────────── 8. RISK RULES ────────────────
    risk_rules = [
        RiskRuleModel(id=RR_LUA_ID, crop_type_id=CT_LUA_ID,
                      min_temperature=20.0, max_temperature=35.0,
                      min_humidity=60.0, max_humidity=90.0,
                      min_soil_moisture=40.0, max_soil_moisture=80.0,
                      duration_minutes=30),
        RiskRuleModel(id=RR_CAPHE_ID, crop_type_id=CT_CAPHE_ID,
                      min_temperature=18.0, max_temperature=28.0,
                      min_humidity=70.0, max_humidity=85.0,
                      min_soil_moisture=50.0, max_soil_moisture=75.0,
                      duration_minutes=60),
        RiskRuleModel(id=RR_TIEU_ID, crop_type_id=CT_TIEU_ID,
                      min_temperature=22.0, max_temperature=32.0,
                      min_humidity=65.0, max_humidity=80.0,
                      min_soil_moisture=45.0, max_soil_moisture=70.0,
                      duration_minutes=45),
        RiskRuleModel(id=RR_CHANHDAY_ID, crop_type_id=CT_CHANHDAY_ID,
                      min_temperature=20.0, max_temperature=30.0,
                      min_humidity=60.0, max_humidity=85.0,
                      min_soil_moisture=50.0, max_soil_moisture=80.0,
                      duration_minutes=30),
    ]
    session.add_all(risk_rules)

    await session.commit()
    logger.info("[Seed] ✅ Seed dữ liệu mẫu thành công!")
    logger.info("[Seed] Tài khoản mẫu (mật khẩu: Abc@1234):")
    logger.info("[Seed]   - farmer1@ocop.vn (Nông dân 1)")
    logger.info("[Seed]   - farmer2@ocop.vn (Nông dân 2)")
    logger.info("[Seed]   - trader@ocop.vn  (Thương lái)")
    logger.info("[Seed]   - distributor@ocop.vn (Nhà phân phối)")
