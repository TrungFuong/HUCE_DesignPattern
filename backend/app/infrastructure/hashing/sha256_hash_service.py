import hashlib
import json

from app.domain.interfaces.services.hash_service import HashService


class Sha256HashService(HashService):

    def hash_data(self, data: dict) -> str:
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()
