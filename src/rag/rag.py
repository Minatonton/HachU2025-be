from textwrap import dedent

from jinja2 import Template
from openai import OpenAI

from src.rag.client import client
from src.rag.model import ChatModel, ImageInfo, RagResponse
from src.rag.search import search_with_filter
from src.rag.search_model import SearchModel


class RAG:
    def __init__(self, collection_name_text: str, collection_name_image: str):
        self.collection_name_text = collection_name_text
        self.collection_name_image = collection_name_image
        self.client = client
        self.openai_client = OpenAI()

    def get_resonse(self, chat_history: list[ChatModel]) -> RagResponse:
        text_search_results = self.get_info_from_rag(
            mode=SearchModel.TEXT, query=chat_history[-1].content
        )
        image_search_results = self.get_info_from_rag(
            mode=SearchModel.IMAGE_TEXT, query=chat_history[-1].content
        )
        prompt = self.get_promt(text_search_results, image_search_results, chat_history)
        return self.chat_from_info(prompt, text_search_results, image_search_results)

    def get_info_from_rag(
        self, mode: SearchModel, query: str, limit_text: int = 1, limit_image: int = 1
    ) -> list[ImageInfo]:
        collection_name = (
            self.collection_name_text if mode == SearchModel.TEXT else self.collection_name_image
        )
        limit = limit_text if mode == SearchModel.TEXT else limit_image
        return search_with_filter(query, limit=limit, collection_name=collection_name)

    def get_promt(
        self,
        text_search_results: list[ImageInfo],
        image_search_results: list[ImageInfo],
        chat_history: list[ChatModel],
    ) -> str:
        # 画像情報も載せておく(TPMの上限上、あまりしたくはない)
        prompt_template = Template("""
        会話履歴:
        {% for chat in chat_history %}
        {{chat}}
        {% endfor %}
        また、回答する際は以下の情報を参考に回答してください
        テキストによる検索結果:
        {% for text_search_result in text_search_results %}
        {{text_search_result.info}}
        {% endfor %}
        画像による検索結果:
        {% for image_search_result in image_search_results %}
        {{image_search_result.info}}
        {% endfor %}
        """)
        prompt = prompt_template.render(
            text_search_results=text_search_results,
            image_search_results=image_search_results,
            chat_history=chat_history,
        )
        return dedent(prompt)

    def chat_from_info(
        self,
        prompt: str,
        text_seaerch_results: list[ImageInfo],
        image_search_results: list[ImageInfo],
    ) -> RagResponse:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下の会話履歴に対する適切な回答を生成してください"},
                {"role": "user", "content": prompt},
            ],
        )
        response_content = response.choices[0].message.content
        assert isinstance(response_content, str)
        return RagResponse(
            response=response_content,
            used_info_by_image=image_search_results,
            used_info_by_text=text_seaerch_results,
        )


if __name__ == "__main__":
    rag = RAG(
        collection_name_text="text_search_model_sample1",
        collection_name_image="image_search_model_sample",
    )
    response = rag.get_resonse(
        [
            ChatModel(role="user", content="こんにちは"),
            ChatModel(role="user", content="こんばんは。犬の画像が欲しいけど、その画像の犬種は?"),
        ]
    )
    print(response)
    client.close()
