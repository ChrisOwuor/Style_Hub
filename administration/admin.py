from django.contrib import admin
from .models import ApprovalRequest


class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'date', 'status', 'created_at', 'stylist_id')


admin.site.register(ApprovalRequest, ApprovalRequestAdmin)
