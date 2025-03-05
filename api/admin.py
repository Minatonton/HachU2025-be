from django.contrib import admin

from api.models import Chat, Diary, DiaryImage, DiaryTag, Section, Tag

admin.site.register(Chat)
admin.site.register(DiaryImage)
admin.site.register(DiaryTag)
admin.site.register(Diary)
admin.site.register(Section)
admin.site.register(Tag)
