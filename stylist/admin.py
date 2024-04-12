

from django.contrib import admin
from .models import Document, UserResponse, Questionnaire


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_picture',
                    'national_id_front', 'national_id_back', 'good_conduct_cert', 'stylist_id']
    list_filter = ['stylist_id']


admin.site.register(Document, DocumentAdmin)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'stylist_id', 'questionnaire_id']
    list_filter = ['stylist_id']


admin.site.register(UserResponse, ResponseAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', ]


admin.site.register(Questionnaire, QuestionnaireAdmin)
