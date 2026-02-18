from httpx import AsyncClient

from src.schemas.products import ProductDto, ProductResponse
from src.settings import settings


class ProductsApi:
    @staticmethod
    async def create(product_dto: ProductDto) -> ProductResponse:
        product_dto = product_dto.model_dump()
        async with AsyncClient() as client:
            resp = await client.post(
                url=f'{settings.SHOP_BACKEND_API_URL}/products/',
                json=product_dto,
            )
            resp.raise_for_status()
            return ProductResponse.model_validate(resp.json())
