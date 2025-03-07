from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Schedule:
    pass


class ScheduleGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate(self):
        return

    def _search(self):
        """dbを検索"""
        return

    def _suggest(self):
        return
