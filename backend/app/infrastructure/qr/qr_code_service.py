import os
import qrcode


class QrCodeService:

    async def generate_for_batch(self, batch_id: str) -> str:
        output_dir = os.path.join("./qrcodes")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{batch_id}.png")
        qrcode.make(f"batch_id:{batch_id}").save(path)
        return path
