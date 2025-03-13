from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from src.rag.utils import image_url_to_base64

load_dotenv()


class Idea(BaseModel):
    content: str


class ImageGenInfo(BaseModel):
    ideas: list[Idea]
    best_idea: Idea
    english_prompt: str


class ImageGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate(self, diary_text: str) -> str:
        """promptからimg生成し,urlを返す"""
        prompt = self._gen_prompt(diary_text)
        return self._call_api(prompt)

    def gen_base64(self, diary_text: str) -> str:
        """base64で返す"""
        prompt = self._gen_prompt(diary_text)
        url = self._call_api(prompt)
        print(url)

        return image_url_to_base64(url, max_height=1000, max_width=1000)

    def _gen_prompt(self, diary_text: str) -> str:
        system_prompt = "あなたはデザイナーです。DALL-E3でイメージに沿った画像を生成するためのプロンプトを作成してください。"
        user_prompt = f"""
        # 前提条件
        DALL-E3で日記の内容を想起指せるような画像を生成するためのプロンプトを生成したいです。

        # 指示
        画像生成のプロンプトを考える際には以下のステップを段階的に踏んでください。
        STEP1: [日記の内容]のイメージのアイデアを箇条書きで6つアイデアブレストして作成してください。
        STEP2: アイデアに対して適切な表現やタッチを選択し、その後配色、構図を決めてください。
        STEP3: ブレストしたアイデアを評価して日記の内容を想起させる最適ものを1つを選んでください。
        STEP4: [プロンプトの条件]に従って最適なアイデアを描写するためのプロンプトを英語で作成してください。

        # プロンプトの条件
        - 日記の内容を想起させるものにしてください
        - 現実味のあるものにしてください(重要)
        - 人の描写は避けてください

        # 日記の内容
        {diary_text}
        """
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": dedent(user_prompt)},
            ],
            response_format=ImageGenInfo,
        )
        img_gen_info = response.choices[0].message.parsed
        assert isinstance(img_gen_info, ImageGenInfo)

        # print(img_gen_info.ideas)
        # print(img_gen_info.best_idea)
        # print(img_gen_info.english_prompt)

        return img_gen_info.english_prompt

    def _call_api(self, prompt: str) -> str:
        """apiを呼ぶ"""
        # (わんちゃん別のモデルとかいろいろ試せるようにgenerateと分けたけど多分あんま意味ない)
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        assert response.data[0].url

        return response.data[0].url


if __name__ == "__main__":
    img_geterator = ImageGenerator()
    base64 = img_geterator.gen_base64(
        "北海道に行って海鮮丼を食べました。マグロとサーモンが載っていておいしかったです。"
    )
    print(base64[:100])
