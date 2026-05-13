# OCOP Traceability System - Backend

Hệ thống truy xuất nguồn gốc chủ động cho sản phẩm OCOP, nông sản chế biến.

## Tech Stack

- **FastAPI** - REST API framework
- **SQL Server** - Relational database (User, Farm, Batch, Shipment, Container, RiskRule)
- **MongoDB** - NoSQL database (SensorLog, BlockchainRecord)
- **Redis** - Message queue buffer
- **MQTT HiveMQ** - IoT sensor data ingestion
- **Ethereum Ganache + Solidity + Web3.py** - Blockchain integrity verification
- **JWT** - Role-based authentication (Farmer, Distributor, Importer, Admin)

## Architecture

Clean Architecture: Domain → Application → Infrastructure → Presentation

## Design Patterns

1. Singleton
2. Factory Method
3. Builder
4. Adapter
5. Facade
6. Proxy
7. Strategy
8. Observer
9. Command
10. Chain of Responsibility

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
