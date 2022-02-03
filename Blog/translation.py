from modeltranslation.translator import register, TranslationOptions
from Blog.models import News

@register(News)
class NewsTranslation(TranslationOptions):
    """Подключение перевода для полей"""
    fields = ('title', 'description')



