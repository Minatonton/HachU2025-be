from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class GenImageView(APIView):
    def post(self, request, *args, **kwargs):
        json_data = request.data
        text: str = json_data.get("text")
        image_uri = ""
        return Response({"image_uri": image_uri})
