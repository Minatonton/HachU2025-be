from pprint import pprint

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class Schedule(BaseModel):
    title: str
    content: str
    url: str


class ScheduleResponce(BaseModel):
    schedules: list[Schedule]


"""
web_search_options={
        "user_location": {
            "type": "approximate",
            "approximate": {
                "country": "JP",
                "city": "Osaka",
                "region": "Osaka",
            },
        },
    },
"""
client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o-search-preview",
#     web_search_options={},
#     messages=[
#         {
#             "role": "user",
#             "content": "出町柳駅付近でいい飲食店は?",
#         }
#     ],
# )
# print(completion.choices[0].message.content)


completion = client.beta.chat.completions.parse(
    model="gpt-4o-search-preview",
    web_search_options={},
    messages=[
        {
            "role": "system",
            "content": "ユーザーにお勧めする予定を複数答えてください。それぞれtitle,content,urlを記述してください(contentにはurlを記述しないでください)",
        },
        {
            "role": "user",
            "content": "京大付近でいい飲食店は?",
        },
    ],
    response_format=ScheduleResponce,
)

res = completion.choices[0].message.parsed
pprint(res)
