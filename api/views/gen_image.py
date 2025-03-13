from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from src.image_generator import ImageGenerator

User = get_user_model()


class GenImageView(APIView):
    def post(self, request, *args, **kwargs):
        json_data = request.data
        text: str = json_data.get("content")
        print(text)
        # これ題名もとってきて文章と合成して渡す方がいい。多分。
        img_gen = ImageGenerator()
        image = img_gen.gen_base64(text)

        # api 登録してない場合は、img_generator, genbase64のとこをコメントアウトして以下を代わりに実行
        # 代わりに表示する画像は自分で適当に変えてください。
        # =========ここから=============
        # import time
        # from src.rag.utils import image_url_to_base64

        # image = image_url_to_base64(
        #     "http://localhost:8000/media/image/diary/5c5d83ac-23de-434a-b6b6-6f3cc4aeae71.jpg",
        #     max_height=1000,
        #     max_width=1000,
        # )
        # time.sleep(5)
        # =========ここまで=============

        return Response({"image": image}, status=200)
