from django.contrib import admin

from .models import Poll, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ["question", "created_by", "pub_date"]
    readonly_fields = ["pub_date"]


admin.site.register(Choice)
