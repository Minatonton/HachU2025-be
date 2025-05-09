import json

from duckduckgo_search import DDGS

# クエリ
with DDGS() as ddgs:
    results = list(
        ddgs.text(
            keywords="大阪 梅田 観光",  # 検索ワード
            region="jp-jp",  # リージョン 日本は"jp-jp",指定なしの場合は"wt-wt"
            safesearch="off",  # セーフサーチOFF->"off",ON->"on",標準->"moderate"
            timelimit=None,  # 期間指定 指定なし->None,過去1日->"d",過去1週間->"w",
            # 過去1か月->"m",過去1年->"y"
            max_results=4,  # 取得件数
        )
    )

# レスポンスの表示
for line in results:
    print(json.dumps(line, indent=2, ensure_ascii=False))

"""
# 出町柳 飲食店
{
  "title": "出町柳駅でおすすめのグルメ情報をご紹介! | 食べログ",
  "href": "https://tabelog.com/kyoto/A2601/A260302/R6479/rstLst/",
  "body": "日本最大級のグルメサイト「食べログ」では、出町柳駅で人気のお店 388件を掲載中。実際にお店で食事をしたユーザーの口コミ、写真、評価など食べログにしかない情報が満載。ランチでもディナーでも、失敗しないみんながおすすめするお"
}
{
  "title": "出町柳のご飯で行きたい!美味しい人気店20選 - Retty（レッティ）",
  "href": "https://retty.me/area/PRE26/ARE116/SUB11504/PUR45/",
  "body": "「出町柳 ご飯」の人気店・穴場のお店など20選+αを紹介。 実名で信頼できる口コミから、あなたにあったお店探しを楽しめます。"
}
{
  "title": "京都・出町柳のおすすめランチ12選!和食の名店、おしゃれな ...",
  "href": "https://haraheri.net/article/1122/demachiyanagi_lunch",
  "body": "今回は出町柳駅周辺でランチにおすすめのお店を和食・洋食・カフェ・中華などジャンル別にご紹介します。 蔵を丸ごと改築した和モダンなイタリアンレストランや、デートや女子会にも利用しやすいおしゃれカフェ、「現代の名工」に選ばれた店主"
}
{
  "title": "出町柳駅でおすすめの美味しいレストランをご紹介! | 食べログ",
  "href": "https://tabelog.com/kyoto/A2601/A260302/R6479/rstLst/RC/",
  "body": "日本最大級のグルメサイト「食べログ」では、出町柳駅で人気のレストランのお店 233件を掲載中。実際にお店で食事をしたユーザーの口コミ、写真、評価など食べログにしかない情報が満載。ランチでもディナーでも、失敗しないみんながお"
}


大阪 梅田 観光
{
  "title": "梅田の観光スポット17選!定番・穴場・名物グルメまで完全攻略 ...",
  "href": "https://osakalucci.jp/umeda-kankou",
  "body": "梅田は西日本最大の繁華街で、お買い物や遊びに行くならおすすめのエリアです。空中庭園やお初天神、HEP FIVE 観覧車などの定番スポットから、水の時計や新梅田食道街などの穴場スポットまで、梅田の魅力を完全攻略します。"
}
{
  "title": "【2024年最新】梅田で外せない観光スポット21選!モデルコース ...",
  "href": "https://newt.net/jpn/osaka/mag-662029200",
  "body": "梅田スカイビルや梅田芸術劇場などの有名な観光地から、穴場スポットまで厳選した梅田エリアのおすすめ観光スポットを紹介します。人気ランキングやモデルコースも参考にして、梅田旅行を楽しみましょう。"
}
{
  "title": "【2023年】大阪市民が教える梅田観光でやっておくべきこと11選 ...",
  "href": "https://livejapan.com/ja/in-kansai/in-pref-osaka/in-umeda_osaka-station_kitashinchi/article-a2000466/",
  "body": "梅田は大阪の玄関口で、商業施設や観光スポットが多く、楽しめる街です。観覧車や写真スポット、絶景カフェやグルメ、アートやエンターテイメントなど、梅田で体験できる11つのおすすめスポットを紹介します。"
}
{
  "title": "【大阪・おでかけ】大阪駅・梅田駅周辺のおすすめスポット19選",
  "href": "https://tabiiro.jp/higaeri/article/osaka-ekisyuuhen/",
  "body": "大阪駅・梅田駅周辺のおすすめ観光スポットを厳選して、駅から近い順にご紹介! 誰もが夢中になれる定番スポットからゆっくり過ごせる穴場スポットまで盛りだくさん。近くにはグルメやショッピング施設がある場所も多いので、食事、買い物と"
}
"""
