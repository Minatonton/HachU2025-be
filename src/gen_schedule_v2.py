from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class ScheduleWithURL(BaseModel):
    title: str
    content: str
    url: str

    def __iter__(self):
        # フィールドの値を順に返す
        yield self.title
        yield self.content
        yield self.url


class SuggestedSchedule(BaseModel):
    title: str
    content: str


class ScheduleResponce(BaseModel):
    schedules: list[ScheduleWithURL]
    location: str
    kind: str


def main(text: str) -> list[SuggestedSchedule]:
    """
    userの志望から予定を生成する
    text: userの志望。あってもなくてもよい
    list[str]で予定のリストを返す。
    """

    try:
        schedules = call_api(text)
    except Exception:
        schedules = [
            SuggestedSchedule(
                title="ケニア",
                content="元田中エリアの定食屋。コストパフォーマンスが高く、男子大学生に人気です。\nhttps://campus-map.jp/kyoto/article/037/",
            ),
            SuggestedSchedule(title="エラー", content="エラーが起きました"),
        ]

    return schedules


def call_api(text: str) -> list[SuggestedSchedule]:
    client = OpenAI()
    system_prompt: str = """
    ユーザーにお勧めする予定を複数答えてください。
    それぞれtitle,content,urlを記述してください(contentにはurlを記述しないでください)
    urlは必ずつけてください。
    contentは簡潔にしてください。
    """
    # urlのとこvalidationでもいい

    user_prompt: str = f"""
    # 指示
    - [ユーザーの志望]に基づいて、提案する[条件]を大まかに設定してください。
    - 特に指定のない場合、地域(location)はユーザーの現在地付近としてください
    - 種類(kind)は[観光, ショッピング, 食事, 文化体験]からあなたが最も適切なものを選んでください。
    - 設定した条件に基づいて、適切な予定を5つ提案してください。
    - 予定はできるだけ具体的な場所を指定してください。

    # ユーザーの志望
    {text}

    # ユーザーの現在地
    大阪梅田

    # 条件
    - 地域(location)
    - 種類(kind)
    """

    # 現在地はもともとフロントの方でボタンを押したらとってくる仕様にしたかったが、
    # フロントの負担を考え、一旦ハードコーディング

    # dbからユーザーの傾向分析もやりたかった。

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-search-preview",
        web_search_options={},
        messages=[
            {"role": "system", "content": dedent(system_prompt)},
            {
                "role": "user",
                "content": dedent(user_prompt),
            },
        ],
        response_format=ScheduleResponce,
    )

    res = completion.choices[0].message.parsed
    assert isinstance(res, ScheduleResponce)
    # print(res, end="\n\n\n")
    schedules = res.schedules

    fixed_schedules: list[SuggestedSchedule] = [
        SuggestedSchedule(title=e.title, content=e.content + e.url) for e in schedules
    ]
    return fixed_schedules


if __name__ == "__main__":
    r = main("京大付近の飲食店でなんかたべたい")
    for e in r:
        print(e)
        print("----------")
    pass
