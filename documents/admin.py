from django.contrib import admin
from .models import *


class DutyInline(admin.TabularInline):
    model = Duty


class DocumentAdmin(admin.ModelAdmin):
    inlines = [DutyInline]
    list_display = ['title', 'number', 'status']
    list_filter = ['status']
    search_fields = ['title', 'number']


admin.site.register(Document, DocumentAdmin)
admin.site.register(Duty)
