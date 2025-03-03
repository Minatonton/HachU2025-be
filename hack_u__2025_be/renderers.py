from rest_framework.renderers import JSONRenderer


class UTF8JSONRenderer(JSONRenderer):
    """Renderer which serializes to JSON in UTF-8"""

    charset = "utf-8"
