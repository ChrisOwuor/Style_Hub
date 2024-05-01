

from .models import StyleCategorie, Style, StyleVariation
from django.contrib import admin
from .models import StylistDocument


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_picture',
                    'national_id_front', 'national_id_back', 'good_conduct_cert', 'stylist_id']
    list_filter = ['stylist_id']


admin.site.register(StylistDocument, DocumentAdmin)





class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', ]
    list_filter = ['category_name',]


admin.site.register(StyleCategorie, CategoryAdmin)


class StyleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stylist', 'category',]
    list_filter = ['stylist', 'category']


admin.site.register(Style, StyleAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'style', ]
    list_filter = ['style']


admin.site.register(StyleVariation, VariationAdmin)



