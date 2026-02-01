from httpx import AsyncClient

from src.schemas.files import FilePath
from src.settings import settings


class FilesApi:
    @staticmethod
    async def upload(image: bytes, bot_id: str, user_id: str) -> FilePath:
        async with AsyncClient() as client:
            resp = await client.post(
                url=f'{settings.FILE_STORAGE_API_URL}/files/',
                files={'file': image},
                data={
                    'bot_id': bot_id,
                    'user_id': user_id,
                }
            )
            resp.raise_for_status()
            return FilePath.model_validate(resp.json())
