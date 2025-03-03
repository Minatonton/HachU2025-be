import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hack_u__2025_be.settings.dev")

application = get_wsgi_application()
