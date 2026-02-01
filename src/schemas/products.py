from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    brand: str
    title: str
    price: int
    quantity: int
    image_path: str
