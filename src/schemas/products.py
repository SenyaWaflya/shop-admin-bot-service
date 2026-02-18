from pydantic import BaseModel


class ProductDto(BaseModel):
    brand: str
    title: str
    price: int
    quantity: int
    image_path: str

class ProductResponse(ProductDto):
    id: int
