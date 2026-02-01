from pydantic import BaseModel


class FilePath(BaseModel):
    file_path: str
