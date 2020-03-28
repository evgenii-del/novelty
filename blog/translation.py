from modeltranslation.translator import register, TranslationOptions
from blog.models import Rate

@register(Rate)
class RateTranslationOptions(TranslationOptions):
    fields = ('name',)
