from django.contrib import admin

from Api.models import Booking, Otp, Questionnaire, StylistResponse, Transaction

# Register your models here.


class OtpAdmin(admin.ModelAdmin):
    list_display = ('created_for', 'code', 'is_verified', 'created_at')


admin.site.register(Otp, OtpAdmin)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'stylist_id', 'questionnaire_id']
    list_filter = ['stylist_id']


admin.site.register(StylistResponse, ResponseAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', ]


admin.site.register(Questionnaire, QuestionnaireAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'stylist', 'date', 'time',
                    'status', 'completed', ]
    list_filter = ['status', 'completed']


admin.site.register(Booking, BookingAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'client', 'stylist', 'time', 'date',
                    'amount', 'status', ]
    list_filter = ['status',]


admin.site.register(Transaction, TransactionAdmin)
