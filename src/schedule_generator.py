from textwrap import dedent

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class Schedule(BaseModel):
    title: str
    content: str


class ScheduleResponce(BaseModel):
    schedules: list[Schedule]


class Condition(BaseModel):
    region: str
    kind: str


class SearchResoponse(BaseModel):
    condition: Condition
    search_word: str


class ScheduleGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate(self, text: str) -> list[Schedule]:
        search_word = self._suggest(text)
        url = self._search_web_by_duckduckgo(search_word)

        return self._check_web(url)

    def _gen_by_duckduckgo(self, text: str) -> list[Schedule]:
        search_word = self._suggest(text)
        url = self._search_web_by_duckduckgo(search_word)

        return self._check_web(url)

    def _suggest(self, text: str):
        system_prompt = "あなたはuserに予定を提案する役割です。"
        user_prompt = f"""
        # 指示
        - [ユーザーの志望]に基づいて、提案する[条件]を大まかに設定してください。
        - 特に指定のない場合、地域はユーザーの現在地付近としてください
        - 種類は[観光, ショッピング, 食事, 文化体験]からあなたが最も適切なものを選んでください。
        - 条件に基づいて、google custom search apiで検索をするのに適切なワードを決めてください
        - ユーザーの質問に対して、その回答を効率よく見つけるために検索エンジンに与える検索ワードを抽出し生成してください。
        - [条件]から、主要なキーワードやテーマを識別し、それに関する適切な出力として検索ワードをまとめてください。
        - 各検索ワードは目的の答えや情報を効率的に見つけるための主要要素を含むべきです。
        - 質問の中で英語を指定してきても、検索ワードは日本語で提示してください。
        - 検索ワードの候補を3つ出してください。検索エンジンに与えたときに最も回答を見つける可能性の高い検索ワードを1番目に出してください。

        # ユーザーの志望
        {text}

        # ユーザーの現在地
        大阪府大阪市梅田


        # 条件
        - 地域
        - 種類
        """
        # response = self.client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": dedent(user_prompt)},
        #     ],
        # )
        # print(response.choices[0].message.content)
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": dedent(user_prompt)},
            ],
            response_format=SearchResoponse,
        )
        search_responce = response.choices[0].message.parsed
        assert isinstance(search_responce, SearchResoponse)
        print(search_responce)
        return search_responce.search_word

    def _search_db(self):
        """dbを検索"""
        return

    def _search_web_by_duckduckgo(self, query: str):
        """duckduckgoのweb検索, urlを返す"""
        # 一旦scriptに書いてある
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    keywords=query,  # 検索ワード
                    region="jp-jp",  # リージョン 日本は"jp-jp",指定なしの場合は"wt-wt"
                    safesearch="off",  # セーフサーチOFF->"off",ON->"on",標準->"moderate"
                    timelimit=None,  # 期間指定 指定なし->None,過去1日->"d",過去1週間->"w",
                    # 過去1か月->"m",過去1年->"y"
                    max_results=1,  # 取得件数
                )
            )
        return results[0]["href"]
        # レスポンスの表示

    def _check_web(self, url: str):
        """urlの内容を受け取って観光地や飲食店をformat化する"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {e}")

        soup = BeautifulSoup(response.text, "html.parser")

        # 主要コンテンツを取得（不要なスクリプトやスタイルを削除）
        for tag in soup(["script", "style", "meta"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)  # 改行や余分なスペースを削除
        print(text)

        user_prompt = f"""
        # 指示
        - [参考文書]の場所に関する内容をlist形式でまとめてください。
        - 要素はtitle, contentの形にしてください。
        - contentにはtitleの内容を100字程度で説明してください。

        # 参考文書
        {text}
        """

        # 最終はstructured_outputにします
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "user", "content": dedent(user_prompt)},
            ],
            response_format=ScheduleResponce,
        )
        schedule_responce = response.choices[0].message.parsed
        assert isinstance(schedule_responce, ScheduleResponce)

        return schedule_responce.schedules

    def gen_by_openai_search(self, text: str) -> list[str]:
        return []


"""
idea
緯度、経度取れるなら付近乱択ができるのでは?

クエリを投げる(ユーザーはtextと位置情報を提供)
-> 大まかな条件を設定
(ユーザーの位置情報や、dbに基づく趣味嗜好の分析結果などから決める)
-> web検索や場所検索のapiで検索
(場合によっては並列化, 非同期化)
(web検索ならapiでurl取得, urlからhtml読み取って必要な情報を抜き取るなどけどwebサイトみたら偏りそう)
(google places apiなどの場合、検索ワードからそのまま情報が得られそう,)
-> 最後にまとめて表示する


# sg._check_web("https://osakalucci.jp/umeda-kankou")を行なった結果


以下に、[参考文書]の梅田に関する内容をlist形式でまとめました。

1. **梅田スカイビル 空中庭園展望台**
   - 内容: 地上173mに位置する展望台で、夜景も見事です。観光やデートにも最適なスポット。

2. **お初天神 露天神社**
   - 内容: 縁結びのパワースポットとして知られる神社。『曽根崎心中』の舞台でもあります。

3. **HEP FIVE 観覧車**
   - 内容: 梅田エリアで目立つ真っ赤な観覧車。一人600円で乗車可能で、観光やデートにおすすめ。

4. **泉の広場**
   - 内容: 梅田の地下街にある、以前はセーブポイントと呼ばれていた広場。現在はグルメスポットとしてリニューアル。

5. **風の広場**
   - 内容: JR大阪駅の真上にある眺めの良い休憩スポット。

6. **水の時計**
   - 内容: JR大阪駅の中央南口にある水のアートで、時間や模様を表示。待ち合わせにも最適。

7. **大阪駅前第3ビル 展望スペース**
   - 内容: 32階と33階にある展望スペース。人が少なく、静かに梅田の景色を楽しめる穴場スポット。

8. **たこ焼き**
   - 内容: 梅田では多くのたこ焼き店があり、美味しいたこ焼きを楽しめるスポットを紹介。

9. **お好み焼き**
   - 内容: 大阪のソウルフードとして多くのお好み焼き店があり、観光客や地元の人が集います。

10. **串カツ**
    - 内容: 新世界だけでなく梅田でも美味しい串カツを楽しめる店が多く存在。

11. **新梅田食道街**
    - 内容: JR大阪駅から徒歩1分の場所に位置する、リーズナブルに大阪グルメを楽しめる飲食店街。

12. **大阪市中央公会堂**
    - 内容: 大阪のシンボル的建物で、重要文化財に指定。観光やガイドツアーにおすすめ。

13. **大阪市立科学館**
    - 内容: 世界最大級のプラネタリウムがあり、展示やワークショップも充実。

14. **国立国際美術館**
    - 内容: 地下に広がるアート空間で、国内外の現代アートが展示されています。

15. **中之島バラ園**
    - 内容: バラの季節には満開となり、多くの観光客が訪れるスポット。

16. **大阪天満宮**
    - 内容: 学問の神様として有名な菅原道真を祀る神社。天神祭でも知られています。

17. **天神橋筋商店街**
    - 内容: 日本一長い商店街で、大阪らしい雰囲気を味わえます。

このリストは、梅田エリアの観光やグルメに関する情報を網羅しています。それぞれのスポットで得られる体験を参考に、梅田観光を楽しんでください。"""

if __name__ == "__main__":
    from pprint import pprint

    sg = ScheduleGenerator()
    schedule = sg.generate("どこか東北とかに旅行行きたい。いいプランない？")

    pprint(schedule)
    # sg._suggest()
    # sg._check_web("https://osakalucci.jp/umeda-kankou")
    pass
