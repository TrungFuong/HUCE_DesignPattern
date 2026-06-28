import os
import qrcode

from app.core.config import settings


class QrCodeService:

    async def generate_for_batch(self, batch_id: str) -> str:
        output_dir = os.path.join("./qrcodes")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{batch_id}.png")
        public_url = f"{settings.public_base_url.rstrip('/')}/traceability/{batch_id}/public"
        qrcode.make(public_url).save(path)
        return path
