from pydantic import BaseModel


class ImageInfo(BaseModel):
    image_path: str
    info: str

    def __str__(self) -> str:
        return f"""
画像(Path): {self.image_path}
情報: {self.info}
        """


class RagResponse(BaseModel):
    response: str
    used_info_by_image: list[ImageInfo]
    used_info_by_text: list[ImageInfo]

    def __str__(self) -> str:
        return f"""
回答: {self.response}
使用した画像情報: {self.used_info_by_image}
使用したテキスト情報: {self.used_info_by_text}
        """


class ChatModel(BaseModel):
    role: str
    content: str

    def __str__(self) -> str:
        return f"""
role: {self.role}
content: {self.content}
        """
