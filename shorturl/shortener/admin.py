from django.contrib import admin
from .models import *


class LinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'created_at', 'last_accessed')  # Отображаемые поля


admin.site.register(Link, LinkAdmin)
admin.site.register(CodeState)
admin.site.register(DeletedCode)
