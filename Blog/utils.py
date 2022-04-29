from django.db.models import ObjectDoesNotExist

class DataMixin:

    def check_next_and_prev_pages(self, context: dict) -> dict:
        """Проверка в базе данных наличия прочих статей для отображения"""

        if self.check_prev():
            context['prev'] = True
            context['prev_link'] = self.object.get_prev_absolute_url()

        if self.check_next():
            context['next'] = True
            context['next_link'] = self.object.get_next_absolute_url()

        return context

    def check_prev(self):
        """Отображать кнопку с предыдущей новостью -->"""
        try:
            if self.object.get_prev_absolute_url():
                return True
        except ObjectDoesNotExist as error:
            pass

    def check_next(self):
        """Отображать кнопку со следующей новостью -->"""
        try:
            if self.object.get_next_absolute_url():
                return True
        except ObjectDoesNotExist as error:
            pass
