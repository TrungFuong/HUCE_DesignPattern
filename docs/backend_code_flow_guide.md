# Tài liệu đọc hiểu backend OCOP Traceability

1. Dự án đang giải quyết bài toán gì.
2. Code được chia tầng như thế nào.
3. Một request hoặc một dữ liệu cảm biến đi qua những file/class nào.

---

## 1. Bối cảnh dự án

Tên đề tài:

> Nghiên cứu ứng dụng công nghệ số xây dựng hệ thống truy xuất nguồn gốc chủ động
> cho sản phẩm OCOP, nông sản chế biến.

Bài toán ban đầu là QR code truy xuất nguồn gốc truyền thống thường chỉ chứa dữ
liệu tĩnh. Dữ liệu đó không phản ánh trạng thái thật trong quá trình trồng trọt,
bảo quản, vận chuyển và cũng khó chứng minh là chưa bị chỉnh sửa.

Dự án đề xuất backend có các ý chính:

- Farmer ghi nhận thông tin nông trại, mùa vụ, lô sản phẩm.
- IoT sensor gửi nhiệt độ, độ ẩm, độ ẩm đất theo thời gian thực qua MQTT.
- MongoDB lưu sensor log dạng time-series.
- SQL database lưu dữ liệu quan hệ như user, farm, batch, shipment.
- Redis Queue làm buffer cho các tác vụ bất đồng bộ.
- Blockchain chỉ lưu hash dữ liệu để kiểm tra tính toàn vẹn.
- Importer quét QR để xem toàn bộ lịch sử và kết quả verification.
- Risk classification dùng rule-based, không dùng AI/ML.

Trong source hiện tại, relational database được cấu hình theo SQL Server qua biến
`sqlserver_url`. Giá trị mặc định là placeholder, bạn nên copy
`backend/.env.example` thành `backend/.env` rồi sửa connection string theo máy của mình.

---

## 2. Cấu trúc tổng quan source code

Thư mục chính:

```txt
backend/
  app/
    main.py
    core/
    domain/
    application/
    infrastructure/
    presentation/
    workers/
  smart_contracts/
  tests/
  requirements.txt
  docker-compose.yml
```

Relational database không còn dùng SQLite mặc định. App đang dùng SQL Server
connection string từ `sqlserver_url`.

Ý nghĩa từng tầng:

| Tầng | Vai trò | Ví dụ file |
|---|---|---|
| `presentation` | REST API controller, nhận HTTP request | `app/presentation/api/v1/batch_controller.py` |
| `application` | Use case/business flow | `BatchService`, `TraceabilityFacade`, `IoTPipelineFacade` |
| `domain` | Entity, enum, interface, rule thuần nghiệp vụ | `Batch`, `SensorLog`, `RiskStrategy` |
| `infrastructure` | Kết nối công nghệ thật: DB, Mongo, Redis, MQTT, Blockchain, QR | `SqlBatchRepository`, `MongoSensorLogRepository`, `SmartContractAdapter` |
| `core` | Config, security, dependency provider | `config.py`, `security.py`, `dependencies.py` |
| `workers` | Nơi dự kiến xử lý background jobs | `blockchain_worker.py`, `sensor_worker.py` |

Luồng phụ thuộc đúng theo Clean Architecture:

```txt
Controller
  -> Application Service / Facade
      -> Domain Interface / Entity / Rule
          <- Infrastructure implementation
```

Controller không nên chứa nghiệp vụ phức tạp. Service/facade điều phối nghiệp vụ.
Repository/adapter trong infrastructure chịu trách nhiệm nói chuyện với database,
Redis, MQTT, blockchain.

---

## 3. Entry point của backend

File chạy đầu tiên:

```txt
app/main.py
```

Nội dung rất ngắn:

```python
from app.presentation.api.router import create_app

app = create_app()
```

Nó gọi sang:

```txt
app/presentation/api/router.py
```

`create_app()` tạo FastAPI app và include các router:

- `/auth`
- `/batches`
- `/farms`
- `/risk-rules`
- `/shipments`
- `/sensors`
- `/traceability`

Nói cách khác, khi chạy `uvicorn app.main:app`, FastAPI lấy object `app` trong
`main.py`, object này đã được gắn các API endpoint từ `router.py`.

Khi app startup, `router.py` gọi `init_db()` để tạo các bảng SQLAlchemy nếu chưa
có. Với SQL Server thật, database trong connection string cần tồn tại trước.

---

## 4. Core layer

### 4.1 `config.py`

File:

```txt
app/core/config.py
```

Class `Settings` đọc cấu hình môi trường qua `pydantic-settings`.

Các cấu hình quan trọng:

- `sqlserver_url`: mặc định trỏ tới SQL Server local placeholder
- `mongodb_url`: mặc định `mongodb://localhost:27017`
- `redis_url`: mặc định `redis://localhost:6379/0`
- `mqtt_broker_url`
- `mqtt_topic`
- `blockchain_rpc_url`
- `contract_address`
- `jwt_secret_key`
- `access_token_expire_minutes`

Cuối file có:

```python
settings = Settings()
```

Đây là một dạng Singleton đơn giản: toàn app dùng chung một object settings.

### 4.2 `security.py`

File này xử lý:

- Hash password.
- Verify password.
- Tạo JWT access token.
- Decode JWT access token.

Nó được dùng trực tiếp trong `AuthService`.

### 4.3 `dependencies.py`

File này định nghĩa các provider như:

- `get_db_session()`
- `get_mongo_db()`
- `get_redis()`
- `get_hash_service()`
- `get_qr_service()`
- `get_blockchain_service()`
- `get_traceability_facade()`
- `get_iot_pipeline_facade()`

Về thiết kế, đây là nơi gom Dependency Injection cho FastAPI. Tuy nhiên trong code
hiện tại nhiều controller vẫn tự tạo service/repository trực tiếp thay vì dùng
`Depends(...)`. Vì vậy hãy hiểu `dependencies.py` là thiết kế DI đã có, nhưng chưa
được áp dụng đồng nhất ở toàn bộ controller.

---

## 5. Domain layer

Domain là tầng gần nghiệp vụ nhất và ít phụ thuộc công nghệ nhất.

### 5.1 Entity chính

Các entity nằm ở:

```txt
app/domain/entities/
```

Một số entity quan trọng:

| Entity | Vai trò |
|---|---|
| `User` | Người dùng hệ thống |
| `Farm` | Nông trại/vùng trồng |
| `Batch` | Lô sản phẩm |
| `Shipment` | Vận chuyển |
| `Container` | Thùng/container |
| `SensorLog` | Dữ liệu cảm biến |
| `RiskRule` | Ngưỡng rule đánh giá rủi ro |
| `BlockchainRecord` | Bản ghi hash/transaction |

Ví dụ `Batch` có hành vi nghiệp vụ:

```python
def mark_at_risk(self) -> None:
    self.risk_level = RiskLevel.AT_RISK

def mark_normal(self) -> None:
    self.risk_level = RiskLevel.NORMAL
```

Điểm này đúng tinh thần Domain: trạng thái của batch nên được đổi thông qua hành
vi của entity, không chỉ sửa field bừa bãi ở controller.

### 5.2 Enum

Các enum nằm ở:

```txt
app/domain/enums/
```

Các enum chính:

- `RoleName`
- `BatchStatus`
- `RiskLevel`
- `SensorType`

Ví dụ `RiskLevel` được service dùng để đánh dấu `NORMAL` hoặc `AT_RISK`.

### 5.3 Repository interface

Các interface nằm ở:

```txt
app/domain/interfaces/repositories/
```

Ví dụ:

- `BatchRepository`
- `FarmRepository`
- `ShipmentRepository`
- `SensorLogRepository`
- `RiskRuleRepository`
- `BlockchainRepository`
- `UserRepository`

Application service chỉ cần biết interface, không cần biết dữ liệu đang nằm ở SQL,
MongoDB hay công nghệ khác.

### 5.4 Service interface

Các service interface nằm ở:

```txt
app/domain/interfaces/services/
```

Ví dụ:

- `QrService`
- `HashService`
- `BlockchainClient`
- `QueueClient`
- `MqttClient`
- `TokenService`
- `PasswordHasher`

Infrastructure sẽ implement các interface này.

### 5.5 Rule và Strategy

Các rule nằm ở:

```txt
app/domain/rules/
```

Các strategy hiện có:

- `TemperatureRiskStrategy`
- `HumidityRiskStrategy`
- `SoilRiskStrategy`

`RiskService` gọi tuần tự các strategy này. Nếu một strategy phát hiện sensor log
vượt ngưỡng thì batch được xem là `AT_RISK`.

Ngoài Strategy, file `risk_chain.py` cũng có Chain of Responsibility:

- `RiskHandler`
- `TemperatureRiskHandler`
- `HumidityRiskHandler`
- `SoilRiskHandler`

Nhưng hiện tại chain này chưa được `RiskService` dùng trực tiếp. Nó đang tồn tại
như phần pattern đã chuẩn bị sẵn.

---

## 6. Application layer

Application layer là nơi chứa use case.

### 6.1 Service

Thư mục:

```txt
app/application/services/
```

Các service chính:

| Service | Nhiệm vụ |
|---|---|
| `AuthService` | Register, login, tạo JWT |
| `BatchService` | Tạo batch, lấy batch, đánh dấu batch rủi ro |
| `FarmService` | Tạo farm, lấy farm |
| `ShipmentService` | Tạo shipment, lấy shipment theo batch |
| `SensorService` | Lưu và đọc sensor log |
| `RiskService` | Phân loại risk theo rule |
| `BlockchainService` | Ghi/lấy/verify hash qua blockchain client |
| `TraceabilityService` | Service truy xuất nguồn gốc, hiện ít được dùng hơn facade |
| `DashboardService` | Placeholder cho dashboard |

### 6.2 Facade

Facade gom nhiều service thành một luồng nghiệp vụ lớn.

Các facade:

```txt
app/application/facades/
```

#### `TraceabilityFacade`

Đây là class quan trọng cho flow quét QR/truy xuất nguồn gốc.

Nó làm các bước:

1. Lấy batch bằng `BatchService`.
2. Lấy farm bằng `FarmService`.
3. Lấy shipment bằng `ShipmentService`.
4. Lấy sensor logs bằng `SensorService`.
5. Tạo hash hiện tại bằng `Sha256HashService`.
6. Lấy hash đã lưu trên blockchain bằng `BlockchainService`.
7. So sánh 2 hash.
8. Dùng `TraceResponseBuilder` build response.

#### `IoTPipelineFacade`

Đây là class quan trọng cho flow IoT.

Nó nhận một `SensorLog`, tạo `SensorEvent`, attach các observer rồi notify:

- `MongoSensorObserver`
- `RiskObserver`
- `BlockchainObserver`
- `DashboardObserver`

### 6.3 Builder

Thư mục:

```txt
app/application/builders/
```

Builder chính:

- `TraceResponseBuilder`: build response trả về cho truy xuất nguồn gốc.
- `BatchHashPayloadBuilder`: build payload để hash batch + sensor logs + shipment.
- `BlockchainTransactionBuilder`: chuẩn bị dữ liệu transaction blockchain.

Trong source hiện tại, `TraceabilityFacade` dùng `TraceResponseBuilder`. Còn
`BatchHashPayloadBuilder` đã có nhưng `WriteHashToBlockchainCommand` hiện đang tự
tạo payload dict thay vì dùng builder này.

### 6.4 Observer

Thư mục:

```txt
app/application/observers/
```

Observer phục vụ luồng dữ liệu cảm biến:

```txt
SensorLog
  -> SensorEvent
      -> MongoSensorObserver
      -> RiskObserver
      -> BlockchainObserver
      -> DashboardObserver
```

Ý nghĩa:

- Mongo observer lưu sensor log vào MongoDB.
- Risk observer kiểm tra rủi ro và update batch nếu cần.
- Blockchain observer push job vào Redis queue.
- Dashboard observer hiện là placeholder.

### 6.5 Command

Thư mục:

```txt
app/application/commands/
```

Command chính:

- `SaveSensorLogCommand`
- `ClassifyRiskCommand`
- `WriteHashToBlockchainCommand`
- `CommandDispatcher`

Mục đích của Command Pattern là đóng gói một job có thể chạy bất đồng bộ trong
worker/queue.

`WriteHashToBlockchainCommand` làm:

1. Lấy batch.
2. Lấy sensor logs.
3. Build payload.
4. Hash payload.
5. Gọi `BlockchainService.write_hash(...)`.

---

## 7. Infrastructure layer

Infrastructure là nơi code chạm công nghệ thật.

### 7.1 SQL database

Thư mục:

```txt
app/infrastructure/database/sqlserver/
```

`session.py` tạo SQLAlchemy async session:

```python
engine = create_async_engine(settings.sqlserver_url, future=True, echo=False)
```

Mặc định URL đang là SQL Server placeholder:

```txt
mssql+aioodbc://sa:YourStrong!Passw0rd@localhost:1433/ocop_traceability?driver=ODBC+Driver+17+for+SQL+Server
```

Các model SQLAlchemy nằm trong:

```txt
app/infrastructure/database/sqlserver/models/
```

Các repository nằm trong:

```txt
app/infrastructure/database/sqlserver/repositories/
```

Ví dụ `SqlBatchRepository` implement `BatchRepository`:

- `find_by_id`
- `save`
- `update`
- `find_by_farm_id`

Repository có nhiệm vụ map giữa SQLAlchemy model và domain entity.

### 7.2 MongoDB

Thư mục:

```txt
app/infrastructure/database/mongodb/
```

`mongo_client.py` tạo singleton Mongo client:

```python
_client: AsyncIOMotorClient | None = None
```

`MongoSensorLogRepository` lưu và đọc collection `sensor_logs`.
Khi MongoDB chưa chạy trong môi trường demo, các hàm đọc log sẽ trả danh sách rỗng
để `/traceability/{batch_id}` không bị lỗi 500 chỉ vì thiếu MongoDB.

Flow cơ bản:

```txt
SensorService
  -> SensorLogRepository interface
      -> MongoSensorLogRepository
          -> mongo_db["sensor_logs"]
```

### 7.3 Redis Queue

Thư mục:

```txt
app/infrastructure/queue/
```

`RedisQueueAdapter` implement `QueueClient`.

Các hàm:

- `push(queue_name, data)` dùng `rpush`.
- `pop(queue_name)` dùng `lpop`.

Trong flow IoT, `BlockchainObserver` push job vào queue:

```txt
blockchain_hash_queue
```

### 7.4 MQTT

Thư mục:

```txt
app/infrastructure/mqtt/
```

Các class:

- `HiveMqttClient`
- `MqttMessageAdapter`
- `MqttSubscriber`

`MqttMessageAdapter` chuyển raw MQTT payload JSON thành `SensorLog`.

`MqttSubscriber` subscribe topic:

```txt
ocop/sensors/#
```

Khi nhận message:

```txt
raw MQTT message
  -> MqttMessageAdapter.to_sensor_log()
  -> IoTPipelineFacade.process_sensor_log()
```

### 7.5 Blockchain

Thư mục:

```txt
app/infrastructure/blockchain/
```

Các class:

- `Web3Client`
- `SmartContractAdapter`
- `BlockchainProxy`

`SmartContractAdapter` bọc Web3.py/smart contract thành interface
`BlockchainClient`. Đây là Adapter Pattern.

`BlockchainProxy` bọc thêm cache Redis cho `get_hash`. Đây là Proxy Pattern.
Nếu Redis chưa chạy, proxy sẽ bỏ qua cache và gọi blockchain client trực tiếp.
Nếu chưa cấu hình `contract_address`, blockchain hash trả về `None`.

Luồng đọc hash:

```txt
BlockchainService.get_hash(batch_id)
  -> BlockchainProxy.get_hash(batch_id)
      -> Redis cache nếu có
      -> SmartContractAdapter.get_hash(batch_id) nếu cache miss
```

Luồng ghi hash:

```txt
BlockchainService.write_hash(batch_id, data_hash)
  -> BlockchainProxy.write_hash(...)
      -> SmartContractAdapter.write_hash(...)
      -> delete cache blockchain_hash:{batch_id}
```

### 7.6 QR code

File:

```txt
app/infrastructure/qr/qr_code_service.py
```

`QrCodeService.generate_for_batch(batch_id)` tạo file:

```txt
./qrcodes/{batch_id}.png
```

Nội dung QR hiện tại là:

```txt
batch_id:{batch_id}
```

Trong sản phẩm hoàn chỉnh, QR thường nên encode URL truy xuất, ví dụ
`/traceability/{batch_id}`.

---

## 8. Presentation layer: API controllers

Các controller nằm ở:

```txt
app/presentation/api/v1/
```

### 8.1 Auth API

File:

```txt
auth_controller.py
```

Endpoint:

```txt
POST /auth/register
POST /auth/login
```

Luồng register:

```txt
HTTP request
  -> auth_controller.register()
  -> AuthService.register()
  -> SqlUserRepository.find_by_email()
  -> hash_password()
  -> User entity
  -> SqlUserRepository.save()
  -> create_access_token()
  -> response access_token
```

Luồng login:

```txt
HTTP request
  -> auth_controller.login()
  -> AuthService.login()
  -> SqlUserRepository.find_by_email()
  -> verify_password()
  -> create_access_token()
  -> response access_token
```

### 8.2 Farm API

File:

```txt
farm_controller.py
```

Endpoint:

```txt
POST /farms/
```

Luồng:

```txt
CreateFarmRequest
  -> FarmService.create_farm()
  -> Farm entity
  -> SqlFarmRepository.save()
```

### 8.3 Batch API

File:

```txt
batch_controller.py
```

Endpoint:

```txt
POST /batches/
GET /batches/{batch_id}
```

Luồng tạo batch:

```txt
CreateBatchRequest
  -> BatchService.create_batch()
  -> Batch entity status=CREATED, risk_level=NORMAL
  -> SqlBatchRepository.save()
  -> QrCodeService.generate_for_batch()
  -> SqlBatchRepository.update(qr_code_url)
  -> response Batch
```

`id` của farm, batch, shipment và risk rule hiện là optional ở DTO. Nếu request
không gửi `id`, service/controller sẽ tự sinh UUID để thuận tiện khi demo API.

### 8.4 Shipment API

File:

```txt
shipment_controller.py
```

Endpoint:

```txt
POST /shipments/
```

Luồng:

```txt
CreateShipmentRequest
  -> ShipmentService.create_shipment()
  -> Shipment entity
  -> SqlShipmentRepository.save()
```

### 8.5 Risk Rule API

File:

```txt
risk_rule_controller.py
```

Endpoint:

```txt
POST /risk-rules/
GET /risk-rules/{crop_type}
```

Luồng tạo rule:

```txt
RiskRuleRequest
  -> RiskRule entity
  -> SqlRiskRuleRepository.save()
```

Rule này được `RiskService` dùng để đánh giá sensor log theo `crop_type`.

### 8.6 Sensor API

File:

```txt
sensor_controller.py
```

Endpoint:

```txt
POST /sensors/
```

Luồng:

```txt
SensorLogRequest
  -> SensorService.save_sensor_log()
  -> MongoSensorLogRepository.save()
  -> MongoDB sensor_logs
```

Lưu ý: endpoint này lưu trực tiếp sensor log vào MongoDB. Nó không đi qua
`IoTPipelineFacade`, nên không tự chạy risk observer hoặc blockchain observer.
Luồng đầy đủ IoT nằm ở MQTT subscriber.

### 8.7 Traceability API

File:

```txt
traceability_controller.py
```

Endpoint:

```txt
GET /traceability/{batch_id}
```

Luồng:

```txt
batch_id
  -> TraceabilityFacade.trace_batch(batch_id)
  -> BatchService.get_by_id()
  -> FarmService.get_by_id()
  -> ShipmentService.get_by_batch_id()
  -> SensorService.get_logs_by_batch_id()
  -> Sha256HashService.hash_data()
  -> BlockchainService.get_hash()
  -> TraceResponseBuilder
  -> response gồm batch, farm, shipment, sensor_logs, is_verified
```

---

## 9. Các luồng nghiệp vụ chính

### 9.1 Luồng tạo tài khoản

```txt
POST /auth/register
  -> AuthController
  -> AuthService
  -> UserRepository.find_by_email
  -> hash password
  -> tạo User entity
  -> UserRepository.save
  -> tạo JWT
  -> trả access_token
```

Điểm cần nhớ:

- Role lấy từ request, nếu không có thì mặc định `FARMER`.
- Password không lưu plain text mà lưu `password_hash`.
- Response trả token để client gọi API sau đó.

### 9.2 Luồng tạo farm

```txt
POST /farms/
  -> FarmController
  -> FarmService
  -> tạo Farm entity
  -> SqlFarmRepository.save
  -> SQL database
```

Farm là dữ liệu nền để batch trỏ tới qua `farm_id`.

### 9.3 Luồng tạo batch và QR

```txt
POST /batches/
  -> BatchController
  -> BatchService.create_batch
  -> tạo Batch entity
  -> lưu DB
  -> tạo QR PNG
  -> update qr_code_url
  -> trả batch
```

Batch lúc mới tạo:

- `status = CREATED`
- `risk_level = NORMAL`

Nếu sau này sensor vượt ngưỡng, `RiskObserver` hoặc `ClassifyRiskCommand` có thể
gọi `BatchService.mark_batch_at_risk()`.

### 9.4 Luồng sensor qua HTTP

```txt
POST /sensors/
  -> SensorController
  -> SensorService
  -> MongoSensorLogRepository
  -> MongoDB
```

Đây là flow ngắn, phù hợp test nhanh API lưu sensor.

Nhưng nó chưa đại diện cho flow chủ động của hệ thống, vì không push blockchain
job và không classify risk.

### 9.5 Luồng sensor qua MQTT đầy đủ

```txt
IoT Sensor / Wokwi
  -> HiveMQ MQTT Broker
  -> MqttSubscriber
  -> MqttMessageAdapter
  -> SensorLog entity
  -> IoTPipelineFacade
  -> SensorEvent.notify()
      -> MongoSensorObserver
      -> RiskObserver
      -> BlockchainObserver
      -> DashboardObserver
```

Chi tiết từng observer:

```txt
MongoSensorObserver
  -> MongoSensorLogRepository.save()
  -> sensor_logs collection

RiskObserver
  -> RiskService.classify_sensor_log()
  -> Temperature/Humidity/Soil strategy
  -> nếu AT_RISK thì BatchService.mark_batch_at_risk()

BlockchainObserver
  -> RedisQueueAdapter.push("blockchain_hash_queue", data)

DashboardObserver
  -> hiện là placeholder
```

### 9.6 Luồng worker ghi blockchain

Theo thiết kế, Redis queue sẽ được worker xử lý:

```txt
Redis blockchain_hash_queue
  -> BlockchainWorker / CommandWorker
  -> WriteHashToBlockchainCommand
  -> BatchService.get_by_id()
  -> SensorService.get_logs_by_batch_id()
  -> Sha256HashService.hash_data()
  -> BlockchainService.write_hash()
  -> BlockchainProxy
  -> SmartContractAdapter
  -> Ethereum/Ganache smart contract
```

Trong source hiện tại, command đã có, nhưng `app/workers/blockchain_worker.py` mới
chỉ là placeholder comment. Nghĩa là kiến trúc đã chuẩn bị nhưng worker thật chưa
được implement đầy đủ.

### 9.7 Luồng importer quét QR/truy xuất

Ý tưởng nghiệp vụ:

```txt
Importer quét QR
  -> lấy batch_id
  -> GET /traceability/{batch_id}
```

Code xử lý:

```txt
TraceabilityController
  -> TraceabilityFacade
      -> đọc batch từ SQL
      -> đọc farm từ SQL
      -> đọc shipment từ SQL
      -> đọc sensor logs từ MongoDB
      -> hash dữ liệu hiện tại
      -> đọc hash trên blockchain
      -> so sánh
      -> build response
```

Kết quả trả về gồm:

- `batch`
- `farm`
- `shipment`
- `sensor_logs`
- `is_verified`

`is_verified = True` nghĩa là hash dữ liệu hiện tại khớp với hash trên blockchain.
Nếu dữ liệu trong DB/Mongo bị sửa sau khi ghi blockchain, hash mới sẽ khác và
`is_verified = False`.

---

## 10. Mapping design patterns trong code

| Pattern | File/class | Đang dùng như thế nào |
|---|---|---|
| Singleton | `settings`, Mongo client, cached dependencies | Dùng chung config/client |
| Repository | `SqlBatchRepository`, `MongoSensorLogRepository` | Tách logic lưu trữ khỏi service |
| Adapter | `SmartContractAdapter`, `RedisQueueAdapter`, `MqttMessageAdapter` | Bọc thư viện/công nghệ ngoài thành interface nội bộ |
| Facade | `TraceabilityFacade`, `IoTPipelineFacade` | Gom nhiều service/observer thành một use case |
| Builder | `TraceResponseBuilder`, `BatchHashPayloadBuilder` | Build response/payload theo từng bước |
| Observer | `SensorEvent`, các `*Observer` | Một sensor log kích hoạt nhiều xử lý phụ |
| Command | `WriteHashToBlockchainCommand`, `SaveSensorLogCommand` | Đóng gói job để worker/dispatcher chạy |
| Strategy | `TemperatureRiskStrategy`, `HumidityRiskStrategy`, `SoilRiskStrategy` | Thay đổi cách đánh giá risk theo loại rule |
| Chain of Responsibility | `risk_chain.py` | Đã có class chain, nhưng chưa tích hợp chính vào service |
| Proxy | `BlockchainProxy` | Cache kết quả đọc blockchain bằng Redis |

---

## 11. Những điểm code hiện tại cần chú ý

Đây không phải là lỗi nhất thiết phải sửa ngay, nhưng là các điểm quan trọng để
hiểu đúng trạng thái source.

### 11.1 Controller chưa dùng DI đồng nhất

`core/dependencies.py` đã có nhiều provider, nhưng controller hiện tự tạo session,
repository và service. Ví dụ `batch_controller.py` tự tạo:

```python
BatchService(SqlBatchRepository(session), QrCodeService())
```

Nếu muốn code sạch hơn, có thể chuyển controller sang dùng `Depends(...)`.

### 11.2 Traceability đã dùng DI, nhưng vẫn cần deploy contract

Controller truy xuất hiện nên đi qua `get_traceability_facade()` trong
`core/dependencies.py` thay vì tự tạo `SmartContractAdapter(..., None)`.

Tuy nhiên verification blockchain chỉ chạy thật khi `.env` có `contract_address`
hợp lệ và smart contract đã deploy lên Ganache/Ethereum. Smart contract trong
`smart_contracts/TraceabilityContract.sol` hiện đã có `storeHash` và `getHash`.

### 11.3 Worker blockchain chưa implement đầy đủ

`WriteHashToBlockchainCommand` đã có, `RedisQueueAdapter` đã có, nhưng
`app/workers/blockchain_worker.py` hiện chỉ có comment. Vì vậy flow Redis queue ->
blockchain trong proposal là flow thiết kế, chưa hoàn thiện trong runtime.

### 11.4 Risk comparison đã được thống nhất theo enum

`RiskObserver` và `ClassifyRiskCommand` nên so sánh với enum:

```python
if risk_level == RiskLevel.AT_RISK:
```

### 11.5 Risk rule cần crop type trong flow đầy đủ

Trong luồng IoT, `RiskObserver` có thể lấy `batch -> farm -> crop_type` rồi truyền
vào `RiskService.classify_sensor_log(...)`. Nếu gọi `RiskService` trực tiếp mà
không truyền `crop_type`, service vẫn fallback về `sensor_log.crop_type` hoặc
`batch_id`, nhưng flow chuẩn nên truyền crop type thật.

### 11.6 Mongo document đã bỏ `_id` khi map về dataclass

Các repository Mongo bỏ field `_id` trước khi tạo `SensorLog` hoặc
`BlockchainRecord`, vì dataclass domain không có field `_id`.

### 11.7 `docker-compose.yml` mới là TODO

Proposal nói có thể dùng Docker cho SQL/Mongo/Redis/Ganache, nhưng
`docker-compose.yml` hiện chỉ có comment TODO, chưa cấu hình service thật.

---

## 12. Cách đọc source theo thứ tự dễ hiểu

Nếu bạn mới đọc dự án, nên đi theo thứ tự này:

1. Đọc `app/main.py` và `app/presentation/api/router.py` để biết API nào được expose.
2. Đọc từng controller trong `app/presentation/api/v1/`.
3. Với mỗi controller, nhảy sang service tương ứng trong `app/application/services/`.
4. Từ service, xem entity trong `app/domain/entities/`.
5. Từ service, xem repository interface trong `app/domain/interfaces/repositories/`.
6. Sau đó mới xem repository implementation trong `app/infrastructure/database/...`.
7. Đọc `TraceabilityFacade` để hiểu flow truy xuất nguồn gốc.
8. Đọc `IoTPipelineFacade` + observers để hiểu flow IoT.
9. Đọc commands + queue + blockchain adapter để hiểu flow bất đồng bộ/blockchain.
10. Cuối cùng đọc `core/dependencies.py` để thấy thiết kế DI tổng thể.

---

## 13. Tóm tắt cực ngắn

Backend này là một FastAPI monolith theo hướng Clean Architecture.

Nó quản lý dữ liệu nông trại/lô hàng bằng SQL, lưu dữ liệu cảm biến bằng MongoDB,
nhận sensor qua MQTT, dùng Redis làm queue, dùng rule-based strategy để đánh giá
rủi ro và dùng blockchain để lưu hash kiểm tra tính toàn vẹn.

Luồng quan trọng nhất khi demo:

```txt
Tạo farm
  -> tạo batch
  -> tạo QR
  -> nhận sensor log
  -> đánh giá risk
  -> ghi hash blockchain
  -> importer quét QR
  -> so sánh hash hiện tại với hash trên chain
  -> trả lịch sử truy xuất + is_verified
```

Hiện tại code đã có phần lớn skeleton/pattern. Các API lõi cần SQL Server
connection string hợp lệ để chạy sau khi đổi khỏi SQLite. Một số phần runtime như worker blockchain, Dashboard, Docker
services và triển khai contract lên Ganache vẫn cần hoàn thiện nếu muốn demo
end-to-end thật.
