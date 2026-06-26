# 📋 Tài liệu Tổng quan Hệ thống
# OCOP Traceability — Truy xuất Nguồn gốc Sản phẩm OCOP
### Sử dụng cho Buổi Bảo vệ Đồ án

---

## 1. TỔNG QUAN DỰ ÁN

### Mục tiêu
Xây dựng hệ thống **truy xuất nguồn gốc sản phẩm OCOP** (Chương trình Mỗi xã một sản phẩm) end-to-end, sử dụng công nghệ IoT, Blockchain và Cloud để:
- **Giám sát** điều kiện môi trường (nhiệt độ, độ ẩm, độ ẩm đất) theo thời gian thực
- **Truy xuất** toàn bộ hành trình sản phẩm từ nông trại → vận chuyển → tiêu thụ
- **Xác minh** tính toàn vẹn dữ liệu bằng Blockchain (không thể sửa)
- **Cảnh báo** rủi ro cho lô hàng khi điều kiện vượt ngưỡng

### Các bên tham gia
| Role | Quyền | Mô tả |
|---|---|---|
| **FARMER** | Tạo batch, quản lý farm | Nông dân sản xuất |
| **TRADER** | Xem batch, tạo shipment | Thương lái thu mua |
| **DISTRIBUTOR** | Quản lý container, shipment | Đơn vị phân phối |
| **IMPORTER** | Xem traceability | Nhà nhập khẩu |
| **ADMIN** | Toàn quyền | Quản trị hệ thống |

---

## 2. KIẾN TRÚC HỆ THỐNG

### Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Angular)                        │
│              Dashboard | QR Scanner | Traceability              │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP REST API (JWT Auth)
┌──────────────────────────────▼──────────────────────────────────┐
│                    BACKEND (FastAPI / Python)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Presentation Layer: REST Controllers + Middlewares       │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  Application Layer: Services | Facades | Commands |       │   │
│  │                     Observers | Builders | DTOs           │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  Domain Layer: Entities | Interfaces | Rules | Enums      │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  Infrastructure: SQL Server | MongoDB | Redis | Web3      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────┬─────────────────────────────────┬────────────────────┘
           │                                 │
    ┌──────▼──────┐                   ┌──────▼──────┐
    │  SQL Server │                   │   MongoDB    │
    │  (metadata) │                   │ (sensor logs)│
    └─────────────┘                   └─────────────┘
           │                                 │
┌──────────▼─────────────────────────────────▼────────────────────┐
│                      WORKER PIPELINE                             │
│   SensorWorker ──► RiskClassify ──► BlockchainWorker            │
└──────────────────────────────┬──────────────────────────────────┘
                               │                  │
                        ┌──────▼──────┐    ┌──────▼──────┐
                        │    Redis    │    │  Ganache     │
                        │  (Queues)   │    │ (Blockchain) │
                        └─────────────┘    └─────────────┘
                               ▲
                        ┌──────┴──────┐
                        │  HiveMQTT   │
                        │  (Broker)   │
                        └──────▲──────┘
                               │ MQTT Publish
                        ┌──────┴──────┐
                        │  ESP32      │
                        │  (Wokwi)   │
                        │ Temp/Humid  │
                        └─────────────┘
```

### Clean Architecture (4 tầng)
```
Domain (core)     ← không phụ thuộc vào bất kỳ tầng nào
    ↑
Application       ← phụ thuộc Domain
    ↑
Infrastructure    ← phụ thuộc Domain + Application
    ↑
Presentation      ← phụ thuộc tất cả
```

---

## 3. LUỒNG DỮ LIỆU CHÍNH

### Luồng IoT (Real-time Sensor)

```
[1] ESP32 (Wokwi) đo nhiệt độ/độ ẩm
[2] Publish MQTT message đến broker.hivemq.com
    Topic: ocop/sensors/{batch_id}
    Payload: {"batch_id":"...", "temperature":32.4, "humidity":60.5}

[3] Backend (MqttSubscriber) nhận → MqttMessageAdapter parse JSON → SensorLog entity
[4] Push vào Redis Queue: sensor_log_queue (rpush)

[5] SensorWorker đọc từ Redis (lpop):
    ├─ [5a] Lưu SensorLog vào MongoDB
    ├─ [5b] Classify risk: Normal / AT_RISK
    │        (so sánh với RiskRule trong SQL Server)
    ├─ [5c] Nếu AT_RISK → cập nhật Batch status trong SQL Server
    └─ [5d] Push vào blockchain_hash_queue

[6] BlockchainWorker đọc từ blockchain_hash_queue:
    ├─ Thu thập: Batch + Farm + Shipment + SensorLogs
    ├─ Tạo payload JSON → SHA-256 hash
    └─ Gọi Smart Contract storeHash(batch_id, hash) trên Ganache
```

### Luồng Truy xuất (QR Code)

```
[1] Người tiêu dùng quét QR code trên sản phẩm
[2] Gọi: GET /traceability/{batch_id}/public (không cần đăng nhập)
[3] TraceabilityFacade thu thập:
    ├─ Thông tin Batch (SQL Server)
    ├─ Thông tin Farm + Owner (SQL Server)
    ├─ Danh sách Shipment + Container (SQL Server)
    ├─ Sensor Logs (MongoDB)
    └─ Hash từ Blockchain (Ganache qua Web3)
[4] Trả về JSON đầy đủ → Hiển thị hành trình sản phẩm
```

---

## 4. DESIGN PATTERNS ÁP DỤNG

> ⚠️ **Lưu ý cho buổi bảo vệ:** Đây là phần quan trọng nhất — mỗi pattern giải quyết vấn đề cụ thể của dự án.

---

### 4.1 OBSERVER PATTERN — Xử lý sự kiện cảm biến

**Vấn đề:** Khi nhận dữ liệu cảm biến, cần thực hiện NHIỀU hành động (lưu MongoDB, phân loại risk, gửi blockchain). Nếu viết tuần tự thì code bị phụ thuộc chặt.

**Giải pháp:** Dùng Observer để tách rời — `SensorEvent` notifies các `Observer` độc lập.

```python
# SensorEvent (Observable)
class SensorEvent:
    def attach(self, observer: SensorEventObserver): ...
    async def notify(self):
        for observer in self._observers:
            await observer.update(self.sensor_log)  # gọi song song

# 4 Observers độc lập:
MongoSensorObserver   → lưu vào MongoDB
RiskObserver          → phân loại risk + cập nhật batch
BlockchainObserver    → push vào blockchain queue
DashboardObserver     → log ra dashboard
```

**Khi nào thêm hành động mới:** Chỉ cần tạo class mới implement `SensorEventObserver` rồi `attach()` — không sửa code cũ.

---

### 4.2 STRATEGY PATTERN — Phân loại Risk

**Vấn đề:** Có nhiều loại cảm biến (nhiệt độ, độ ẩm, độ ẩm đất), mỗi loại có logic phân loại risk khác nhau. Không muốn dùng `if-else` dài.

**Giải pháp:** Mỗi loại cảm biến là một Strategy riêng.

```python
class RiskStrategy(ABC):
    @abstractmethod
    def evaluate(self, sensor_log, rule) -> RiskLevel: ...

class TemperatureRiskStrategy(RiskStrategy):
    def evaluate(self, sensor_log, rule):
        if sensor_log.temperature < rule.min_temperature \
           or sensor_log.temperature > rule.max_temperature:
            return RiskLevel.AT_RISK
        return RiskLevel.NORMAL

class HumidityRiskStrategy(RiskStrategy): ...
class SoilMoistureRiskStrategy(RiskStrategy): ...

# RiskService áp dụng tất cả strategies:
class RiskService:
    strategies = [TemperatureRiskStrategy(), HumidityRiskStrategy(), SoilMoistureRiskStrategy()]
    
    async def classify_sensor_log(self, sensor_log) -> RiskLevel:
        for strategy in self.strategies:
            if strategy.evaluate(sensor_log, rule) == RiskLevel.AT_RISK:
                return RiskLevel.AT_RISK
        return RiskLevel.NORMAL
```

**Thêm loại cảm biến mới:** Chỉ cần tạo class strategy mới, không sửa `RiskService`.

---

### 4.3 CHAIN OF RESPONSIBILITY PATTERN — Chuỗi xử lý Risk

**Vấn đề:** Sau khi phân loại, cần xử lý theo chuỗi (nếu handler này không xử lý được thì chuyển sang handler tiếp).

**Giải pháp:** Mỗi loại risk là một Handler trong chuỗi.

```python
class RiskHandler(ABC):
    def set_next(self, handler): self._next = handler
    
    async def handle(self, sensor_log, rules):
        if self._next:
            return await self._next.handle(sensor_log, rules)

class TemperatureRiskHandler(RiskHandler):
    async def handle(self, sensor_log, rules):
        # Kiểm tra temperature
        # Nếu AT_RISK → trả về ngay, không cần kiểm tra tiếp
        # Nếu NORMAL → chuyển sang handler tiếp theo

# Chuỗi: Temperature → Humidity → SoilMoisture
```

---

### 4.4 COMMAND PATTERN — Đóng gói hành động

**Vấn đề:** Các hành động phức tạp (lưu sensor log, ghi blockchain) cần được đóng gói, có thể xếp hàng, retry, log.

**Giải pháp:** Mỗi hành động là một `Command` object, dùng `CommandDispatcher` để thực thi.

```python
class Command(ABC):
    @abstractmethod
    async def execute(self): ...

class SaveSensorLogCommand(Command):
    def __init__(self, sensor_log, sensor_service): ...
    async def execute(self):
        return await self.sensor_service.save_sensor_log(self.sensor_log)

class WriteHashToBlockchainCommand(Command):
    async def execute(self):
        # Thu thập data → hash → ghi lên blockchain

class CommandDispatcher:
    async def dispatch(self, command: Command):
        return await command.execute()

# CommandWorker sử dụng:
save_cmd = SaveSensorLogCommand(sensor_log, sensor_service)
await dispatcher.dispatch(save_cmd)

risk_cmd = ClassifyRiskCommand(sensor_log, risk_service, batch_service)
await dispatcher.dispatch(risk_cmd)
```

---

### 4.5 FACADE PATTERN — Đơn giản hoá giao diện phức tạp

**Vấn đề:** Truy xuất nguồn gốc cần gọi NHIỀU service khác nhau — code controller sẽ rất phức tạp.

**Giải pháp:** `TraceabilityFacade` ẩn đi sự phức tạp, controller chỉ gọi 1 phương thức.

```python
class TraceabilityFacade:
    def __init__(self, batch_service, farm_service, shipment_service,
                 sensor_service, blockchain_service, hash_service, ...):
        # Nhận nhiều service
    
    async def trace_batch(self, batch_id: str):
        batch     = await self.batch_service.get_by_id(batch_id)
        farm      = await self.farm_service.get_by_id(batch.farm_id)
        shipments = await self.shipment_service.get_by_batch_id(batch_id)
        logs      = await self.sensor_service.get_logs_by_batch_id(batch_id)
        hash_     = await self.blockchain_service.get_hash(batch_id)
        return self.trace_response_builder.build(batch, farm, shipments, logs, hash_)

# Controller chỉ cần:
@router.get("/{batch_id}")
async def trace(batch_id, facade = Depends(get_traceability_facade)):
    return await facade.trace_batch(batch_id)   # 1 dòng!
```

**Tương tự:** `IoTPipelineFacade` đơn giản hoá việc notify tất cả Observers.

---

### 4.6 BUILDER PATTERN — Xây dựng response phức tạp

**Vấn đề:** Kết quả truy xuất nguồn gốc là một object lớn với nhiều nested data — khó build inline.

**Giải pháp:** `TraceResponseBuilder` xây dựng từng bước.

```python
class TraceResponseBuilder:
    def build(self, batch, farm, shipments, sensor_logs, blockchain_hash) -> dict:
        return {
            "batch": self._build_batch_section(batch),
            "farm": self._build_farm_section(farm),
            "supply_chain": self._build_supply_chain(shipments),
            "sensor_history": self._build_sensor_section(sensor_logs),
            "blockchain": {
                "hash": blockchain_hash,
                "verified": bool(blockchain_hash)
            }
        }

class BatchHashPayloadBuilder:
    def build(self, batch, farm, shipments, sensor_logs) -> dict:
        # Tạo payload JSON chuẩn để hash SHA-256
```

---

### 4.7 PROXY PATTERN — Cache Blockchain queries

**Vấn đề:** Mỗi lần đọc hash từ Blockchain phải gọi Web3 → chậm và tốn tài nguyên.

**Giải pháp:** `BlockchainProxy` đứng trước `SmartContractAdapter`, cache kết quả vào Redis 5 phút.

```python
class BlockchainProxy(BlockchainClient):   # cùng interface
    def __init__(self, blockchain_client, cache_client):
        self.blockchain_client = blockchain_client  # SmartContractAdapter
        self.cache_client = cache_client            # Redis

    async def get_hash(self, batch_id) -> str | None:
        # Bước 1: Thử đọc từ Redis cache
        cached = await self.cache_client.get(f"blockchain_hash:{batch_id}")
        if cached:
            return cached  # Trả về nhanh!
        
        # Bước 2: Cache miss → gọi blockchain thật
        hash_ = await self.blockchain_client.get_hash(batch_id)
        
        # Bước 3: Lưu vào cache 5 phút
        await self.cache_client.set(f"blockchain_hash:{batch_id}", hash_, ex=300)
        return hash_

    async def write_hash(self, batch_id, data_hash):
        tx = await self.blockchain_client.write_hash(batch_id, data_hash)
        # Xoá cache cũ khi ghi mới:
        await self.cache_client.delete(f"blockchain_hash:{batch_id}")
        return tx
```

**Lợi ích:** Controller và Worker không biết có cache — giao diện giống hệt `BlockchainClient`.

---

### 4.8 REPOSITORY PATTERN — Tách biệt lưu trữ

**Vấn đề:** Nếu business logic gọi thẳng SQL/MongoDB, khi đổi database phải sửa toàn bộ.

**Giải pháp:** Định nghĩa interface (hợp đồng) ở tầng Domain, implement ở Infrastructure.

```python
# Domain Interface (hợp đồng):
class SensorLogRepository(ABC):
    @abstractmethod
    async def save(self, sensor_log: SensorLog) -> SensorLog: ...
    @abstractmethod
    async def find_by_batch_id(self, batch_id: str) -> list[SensorLog]: ...

# Infrastructure — MongoDB:
class MongoSensorLogRepository(SensorLogRepository):
    async def save(self, sensor_log):
        await self.collection.insert_one(sensor_log.__dict__)
        return sensor_log

# Nếu đổi sang PostgreSQL:
class PostgresSensorLogRepository(SensorLogRepository):
    # implement theo cách mới
    # → Service không cần sửa!
```

---

## 5. REDIS — MESSAGE QUEUE

### Tại sao cần Redis?

Khi dữ liệu từ 100 cảm biến gửi cùng lúc:
- **Không có Redis:** Backend cố xử lý 100 requests cùng lúc → timeout, nghẽn
- **Có Redis:** Backend nhận → push queue ngay (nhanh) → Worker xử lý từ từ trong nền

### 2 Queue trong hệ thống

| Queue | Producer | Consumer | Nội dung |
|---|---|---|---|
| `sensor_log_queue` | MqttSubscriber (Backend) | SensorWorker | Raw sensor data từ ESP32 |
| `blockchain_hash_queue` | SensorWorker | BlockchainWorker | batch_id cần ghi blockchain |

### Cấu trúc message trong queue

**sensor_log_queue:**
```json
{
  "id": "uuid-...",
  "batch_id": "3d12cb23-5f4e-444e-a006-6cc035f407a6",
  "temperature": 32.4,
  "humidity": 60.5,
  "soil_moisture": 45.0,
  "recorded_at": "2024-01-15T10:30:00"
}
```

**blockchain_hash_queue:**
```json
{
  "batch_id": "3d12cb23-5f4e-444e-a006-6cc035f407a6",
  "sensor_log_id": "log-uuid-...",
  "reason": "SENSOR_LOG_SAVED"
}
```

### Redis Queue hoạt động như thế nào?

```python
# Push (Producer — FIFO):
await redis.rpush("sensor_log_queue", json.dumps(data))

# Pop (Consumer — blocking):
raw = await redis.lpop("sensor_log_queue")
if raw:
    data = json.loads(raw)
    # xử lý...

# Nếu queue trống → sleep 1 giây rồi thử lại
```

---

## 6. BLOCKCHAIN — SMART CONTRACT

### Smart Contract làm gì?

```solidity
// OcopTraceability.sol
contract OcopTraceability {
    mapping(string => string) private batchHashes;
    
    function storeHash(string memory batchId, string memory dataHash) public {
        batchHashes[batchId] = dataHash;
    }
    
    function getHash(string memory batchId) public view returns (string memory) {
        return batchHashes[batchId];
    }
}
```

Đơn giản: lưu `batchId → SHA256hash` không thể sửa.

### Quy trình ghi Blockchain

```
1. Thu thập dữ liệu: Batch + Farm + Shipments + SensorLogs
2. Serialize thành JSON chuẩn (key sort alphabetically)
3. SHA-256 hash → "a1b2c3d4..."
4. Gọi storeHash(batch_id, hash) → transaction trên Ganache
5. Lưu tx_hash trả về (bằng chứng giao dịch)
```

### Quy trình xác minh

```
1. Đọc hash hiện tại từ DB (batch + farm + sensor logs mới nhất)
2. Tính SHA-256 → "current_hash"
3. Gọi getHash(batch_id) từ blockchain → "stored_hash"
4. So sánh: current_hash == stored_hash?
   → TRUE: dữ liệu nguyên vẹn, không bị sửa
   → FALSE: dữ liệu đã bị thay đổi (cảnh báo!)
```

### Tại sao dùng Blockchain (không chỉ lưu DB)?

| | Database thường | Blockchain |
|---|---|---|
| Ai có thể sửa? | Admin DB | Không ai (immutable) |
| Có thể xoá? | Có | Không |
| Ai xác minh? | Tin tưởng nhà cung cấp | Mạng phi tập trung |
| Tốc độ đọc | Nhanh | Chậm hơn (có cache Redis) |

---

## 7. API ENDPOINTS

### 🔓 Public (không cần đăng nhập)
| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/auth/register` | Đăng ký tài khoản |
| POST | `/auth/login` | Đăng nhập, nhận JWT token |
| GET | `/traceability/{batch_id}/public` | Xem truy xuất nguồn gốc (QR scan) |
| GET | `/blockchain/hash/{batch_id}` | Xem hash blockchain (QR verify) |

### 🔒 Cần JWT Token
| Nhóm | Endpoints |
|---|---|
| **Batches** | CRUD + QR code |
| **Farms** | CRUD |
| **Containers** | CRUD |
| **Crop Types** | CRUD |
| **Shipments** | Tạo + xem |
| **Risk Rules** | CRUD |
| **Sensors** | Xem logs theo batch |
| **Dashboard** | Summary, recent sensors, batch status |
| **Traceability** | Xem đầy đủ (nội bộ) |
| **Blockchain** | Xác minh hash (nội bộ) |
| **Users** | Xem danh sách, GET /me |

---

## 8. TECH STACK

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Backend API | **FastAPI** (Python) | REST API, MQTT listener |
| ORM | **SQLAlchemy** (async) | Kết nối SQL Server |
| NoSQL | **Motor** (async MongoDB driver) | Lưu sensor logs |
| Message Queue | **Redis** + aioredis | Tách Producer/Consumer |
| Blockchain | **Web3.py** + Ganache | Ghi/đọc hash |
| Smart Contract | **Solidity** + Truffle | Logic blockchain |
| IoT Simulator | **Wokwi** + ESP32 | Giả lập cảm biến |
| MQTT Broker | **HiveMQ** (cloud) | Nhận dữ liệu IoT |
| Auth | **JWT** (python-jose) + bcrypt | Xác thực người dùng |
| Database | **SQL Server** | Dữ liệu nghiệp vụ |

---

## 9. CÂU HỎI BẢO VỆ & TRẢ LỜI GỢI Ý

**Q: Tại sao dùng MongoDB cho sensor logs thay vì SQL Server?**

> Sensor logs là dữ liệu time-series, schema có thể thay đổi (thêm loại cảm biến mới), số lượng lớn và cần write nhanh. MongoDB phù hợp hơn SQL Server cho loại dữ liệu này. Dữ liệu nghiệp vụ có cấu trúc cố định (batch, farm, shipment) thì vẫn dùng SQL Server.

**Q: Tại sao cần Redis Queue? Không xử lý thẳng được không?**

> Được, nhưng nếu 1000 cảm biến gửi cùng lúc, backend sẽ phải xử lý 1000 lần ghi MongoDB + gọi blockchain đồng thời → timeout và crash. Redis Queue cho phép nhận nhanh (push queue < 1ms), Worker xử lý tuần tự với tốc độ ổn định.

**Q: Blockchain có thực sự bảo đảm không thể sửa không?**

> Trong dự án dùng Ganache (blockchain local để demo). Trên production sẽ deploy lên Ethereum testnet/mainnet. Bản chất: một khi transaction được confirm, không ai — kể cả admin — có thể sửa giá trị đã ghi. Hash không khớp = cảnh báo dữ liệu bị giả mạo.

**Q: Observer Pattern vs gọi tuần tự trực tiếp — ưu điểm gì?**

> Gọi tuần tự: `save() → classify() → push_blockchain()` — 3 bước phụ thuộc nhau, thêm bước 4 phải sửa code. Observer: `event.notify()` gọi tất cả observers tự động, thêm observer mới không cần sửa code cũ — đây là nguyên tắc Open/Closed trong SOLID.

**Q: Proxy Pattern cho Blockchain giải quyết vấn đề gì?**

> Mỗi lần đọc hash từ blockchain mất 200-500ms (gọi Web3). Nếu trang truy xuất nguồn gốc được 1000 người xem cùng lúc, sẽ có 1000 lần gọi blockchain = cực chậm. BlockchainProxy cache kết quả vào Redis 5 phút: lần đầu 500ms, các lần sau < 1ms.
