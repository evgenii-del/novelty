from django.contrib import admin
from .models import News, Rate, Review
from modeltranslation.admin import TranslationAdmin

@admin.register(Rate)
class RateTranslationAdmin(TranslationAdmin):
    list_display = ('name',)
    
admin.site.register(News)
admin.site.register(Review)
