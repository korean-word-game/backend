from django.contrib import admin
from .models import WordType,WordFile,Word,GameRoom

admin.site.register(WordType)
admin.site.register(Word)
admin.site.register(GameRoom)
