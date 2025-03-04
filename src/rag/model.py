from pydantic import BaseModel


class ImageInfo(BaseModel):
    image_path: str
    info: str

    def __str__(self) -> str:
        return f"""
画像（Path）：　{self.image_path}
情報：　{self.info}
        """