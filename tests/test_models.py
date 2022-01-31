from django.test import TestCase

from Blog.models import News


class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='Title', description='Description')

    def test_title_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Заголовок')

    def test_description_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_date_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_time_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'Время создания')

    def test_draft_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('draft').verbose_name
        self.assertEquals(field_label, 'Черновик')

    def test_poster_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('poster').verbose_name
        self.assertEquals(field_label, 'Постер')

    def test_poster_upload_to_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('poster').upload_to
        self.assertEquals(field_label, 'media/poster/')

    def test_creator_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('creator').verbose_name
        self.assertEquals(field_label, 'Создатель')

    def test_object_name_str(self):
        obj = News.objects.get(id=1)
        expected_object_name = '%s' % (obj.title)
        self.assertEquals(expected_object_name, str(obj))
