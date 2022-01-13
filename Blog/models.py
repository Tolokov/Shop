from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date
from mptt.models import TreeForeignKey, MPTTModel


class News(models.Model):
    """Новости и события, доступ к форме только для пользователей"""
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField('Описание', max_length=5000)
    date = models.DateField('Дата создания', default=date.today)
    time = models.TimeField('Время создания', auto_now=True, null=True)
    draft = models.BooleanField('Черновик', default=False)
    poster = models.ImageField('Постер', upload_to='media/poster/')
    creator = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_post', kwargs={'post_id': self.id})

    def get_prev_absolute_url(self):
        prev_page = self.get_previous_by_date(draft=False).id
        return reverse('single_post', kwargs={'post_id': prev_page})

    def get_next_absolute_url(self):
        next_page = self.get_next_by_date(draft=False).id
        return reverse('single_post', kwargs={'post_id': next_page})

    class Meta:
        verbose_name = 'Новость или событие'
        verbose_name_plural = 'Новости и события'
        ordering = ['-id']


class Comment(MPTTModel):
    """Комментарии к News"""
    text = models.TextField('Коментарий', max_length=1500, blank=False)
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Ответ'
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.news.id} {self.creator}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    class MPTTMeta:
        order_insertion_by = ['created']
