from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ImageGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate(self, prompt: str) -> str:
        """promptからimg生成し,urlを返す"""
        return self._call_api(prompt)

    def _call_api(self, prompt: str) -> str:
        """apiを呼ぶ"""
        # (わんちゃん別のモデルとかいろいろ試せるようにgenerateと分けたけど多分あんま意味ない)
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        assert response.data[0].url

        return response.data[0].url


if __name__ == "__main__":
    img_geterator = ImageGenerator()
    url = img_geterator.generate("白くてふわふわな猫の画像")
    print(url)
    # これクラスにする意味ない気がする
