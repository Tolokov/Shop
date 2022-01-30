from django.db.models import Q
from django.core.serializers import serialize

from logging import getLogger
from json import loads

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
        queryset = serialize("json", self.get_queryset())
        queryset = loads(queryset)
        return queryset

