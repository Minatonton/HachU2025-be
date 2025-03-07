from django.contrib import admin

from api.models import Chat, Diary, DiaryTag, Schedule, Section, Tag

admin.site.register(Chat)
admin.site.register(DiaryTag)
admin.site.register(Diary)
admin.site.register(Section)
admin.site.register(Tag)
admin.site.register(Schedule)
