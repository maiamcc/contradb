from django.contrib import admin
from contratest.models import Dance, Move

class MoveInline(admin.StackedInline):
    model = Move
    extra = 8

class DanceAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'formation', 'progression', 'tags']
    inlines = [MoveInline]

admin.site.register(Dance, DanceAdmin)
