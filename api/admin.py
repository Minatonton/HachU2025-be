from django.contrib import admin

from api.models import Chat, Diary, DiaryTag, Section, Tag

admin.site.register(Chat)
admin.site.register(DiaryTag)
admin.site.register(Diary)
admin.site.register(Section)
admin.site.register(Tag)
