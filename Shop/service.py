from django.db.models import Q, Avg
from django.core import serializers, paginator

from logging import getLogger
from json import loads

from Shop.models import Review

logger = getLogger(__name__)


class JsonHandler:

    def handler(self):
        """Обработчик поступающих запросов к ajax фильтру"""
        if self.request.GET == {}:
            return self.queryset

        elif len(self.request.GET) == 2:
            queryset = self.queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) &
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

        else:
            queryset = self.queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) |
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

    def json_answer(self):
        """Иза ошибки форимирования json ответа, пришлось воспользоваться встроенной библиотекой json"""
        queryset = serializers.serialize("json", self.get_queryset())
        queryset = loads(queryset)
        return queryset


class ProductDetailMixin:

    def get_review_queryset(self, context: dict) -> dict:
        """Формирование средней оценки для продукта на основе оставленных отзывов"""
        review_queryset = Review.objects.filter(product=self.object).select_related('grade')
        context['reviews'] = review_queryset
        context['count'] = review_queryset.__len__()

        if review_queryset:
            avg = review_queryset.aggregate(Avg('grade__value'))['grade__value__avg']
            stars = round(avg)
            context['grade_on'] = range(stars)
            context['grade_off'] = range(5 - stars)
        else:
            context['avg_grade'] = False

        return context

    @staticmethod
    def paginator_optimization(queryset, per_page=3, max_pages=5):
        """Paginator optimization (9 SQL queries --> 6 SQL queries)"""
        list_objects = list(queryset[:per_page * max_pages])
        paginator_object = paginator.Paginator(list_objects, per_page=per_page)
        return paginator_object

    @staticmethod
    def get_user_ip(request):
        """Получение ip пользователя оставившего комментарий"""
        redirected = request.META.get('HTTP_X_FORWARDED_FOR')

        if redirected:
            return redirected.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')

    def save_form(self, form):
        """Сохранение отзыва к товару"""
        if form.is_valid():
            form = form.cleaned_data
            logger.info(f'Получен комментарий к новости{form["product"]} ')
            Review.objects.update_or_create(
                name=form['name'],
                email=form['email'],
                text=form['text'],
                ipaddress=self.get_user_ip(self.request),
                product=form["product"],
                grade=form['grade'],
            )
            logger.info(f'Успешно опубликован комментарий к новости: {form["product"]}')

        else:
            logger.warning(f'Пользователь не смог оставить комментарий, {form}')
