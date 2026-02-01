from httpx import AsyncClient

from src.schemas.products import ProductResponse
from src.settings import settings


class ProductsApi:
    @staticmethod
    async def create(product: dict[str, str | int]) -> ProductResponse:
        async with AsyncClient() as client:
            resp = await client.post(
                url=f'{settings.SHOP_BACKEND_API_URL}/products/',
                json=product,
            )
            resp.raise_for_status()
            return ProductResponse.model_validate(resp.json())
