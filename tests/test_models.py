from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Blog.models import News, Comment
from Shop.models import *


class NewsModelTest(TestCase):
    """Blog.models.News"""

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
        field_upload = obj._meta.get_field('poster').upload_to
        self.assertEquals(field_upload, 'media/poster/')

    def test_creator_label(self):
        obj = News.objects.get(id=1)
        field_label = obj._meta.get_field('creator').verbose_name
        self.assertEquals(field_label, 'Создатель')

    def test_object_str(self):
        obj = News.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'Title')

    def test_get_absolute_url_ru(self):
        obj = News.objects.get(id=1)
        expected_absolute_url = '%s' % obj.get_absolute_url()
        self.assertEquals(expected_absolute_url, '/ru/blog/1/')


class CommentModelTest(TestCase):
    """Blog.models.Comment"""

    @classmethod
    def setUpTestData(cls):
        news = News.objects.create(title='Title', description='Description')
        user = User.objects.create(username='admin')
        Comment.objects.create(text='text', parent=None, creator=user, news=news)

    def test_text_label(self):
        obj = Comment.objects.get(id=1)
        field_label = obj._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Коментарий')

    def test_parent_label(self):
        obj = Comment.objects.get(id=1)
        field_label = obj._meta.get_field('parent').verbose_name
        self.assertEquals(field_label, 'Ответ')

    def test_news_label(self):
        obj = Comment.objects.get(id=1)
        field_label = obj._meta.get_field('news').verbose_name
        self.assertEquals(field_label, 'news')

    def test_creator_label(self):
        obj = Comment.objects.get(id=1)
        field_label = obj._meta.get_field('creator').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_created_label(self):
        obj = Comment.objects.get(id=1)
        field_label = obj._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'created')

    def test_object_str(self):
        obj = Comment.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, '1 admin')


class BrandModelsTest(TestCase):
    """Shop.models.Brand"""

    @classmethod
    def setUpTestData(cls):
        image_path = 'fixtures_data/archive/MK/Logo_MK.jpg'
        image_object = SimpleUploadedFile(
            name='Logo_MK',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg'
        )

        Brand.objects.create(
            name='Michael',
            description='The Michael it is Brand',
            slug='michael',
            image=image_object,
        )

    def test_name_label(self):
        obj = Brand.objects.get(id=1)
        field_label = obj._meta.get_field('name').verbose_name
        self.assertEquals(field_label, "Название бренда")

    def test_name_value(self):
        obj = Brand.objects.get(id=1)
        expected_object_name = '%s' % str(obj.name)
        self.assertEquals(expected_object_name, 'Michael')

    def test_description_label(self):
        obj = Brand.objects.get(id=1)
        field_label = obj._meta.get_field('description').verbose_name
        self.assertEquals(field_label, "Описание")

    def test_description_value(self):
        obj = Brand.objects.get(id=1)
        expected_object_name = '%s' % str(obj.description)
        self.assertEquals(expected_object_name, 'The Michael it is Brand')

    def test_slug_label(self):
        obj = Brand.objects.get(id=1)
        field_label = obj._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, "slug")

    def test_image_upload_to_label(self):
        obj = Brand.objects.get(id=1)
        field_upload = obj._meta.get_field('image').upload_to
        self.assertEquals(field_upload, 'media/brands/')

    def test_object_str(self):
        obj = Brand.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'Michael')


class CategoryModelsTest(TestCase):
    """Shop.models.Category"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Blue', description='Blue jeans', slug='blue', )

    def test_name_label(self):
        obj = Category.objects.get(id=1)
        field_label = obj._meta.get_field('name').verbose_name
        self.assertEquals(field_label, "Название категории")

    def test_name_value(self):
        obj = Category.objects.get(id=1)
        expected_object_name = '%s' % str(obj.name)
        self.assertEquals(expected_object_name, 'Blue')

    def test_description_label(self):
        obj = Category.objects.get(id=1)
        field_label = obj._meta.get_field('description').verbose_name
        self.assertEquals(field_label, "Описание")

    def test_description_value(self):
        obj = Category.objects.get(id=1)
        expected_object_name = '%s' % str(obj.description)
        self.assertEquals(expected_object_name, 'Blue jeans')

    def test_slug_label(self):
        obj = Category.objects.get(id=1)
        field_label = obj._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, "slug")

    def test_object_str(self):
        obj = Category.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'Blue')


class Card_ProductModelsTest(TestCase):
    """Shop.models.Card_Product"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Blue', description='Blue jeans', slug='blue', )
        image_path = 'fixtures_data/archive/MK/Logo_MK.jpg'
        image_object = SimpleUploadedFile(
            name='Logo_MK',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg'
        )

        Brand.objects.create(
            name='Michael',
            description='The Michael it is Brand',
            slug='michael',
            image=image_object,
        )

        Card_Product.objects.create(
            product_public_ID=999000,
            name='Шорты',
            description='Шорты Класические',
            price='100.00',
        )

    def test_object_str(self):
        obj = Card_Product.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'ID: 999000 NAME: Шорты')

    def test_get_absolute_url_ru(self):
        obj = Card_Product.objects.get(id=1)
        expected_absolute_url = '%s' % obj.get_absolute_url()
        self.assertEquals(expected_absolute_url, '/products/1/')


class ProductImageModelsTest(TestCase):
    """Shop.models.ProductImage"""

    @classmethod
    def setUpTestData(cls):
        product = Card_Product.objects.create(
            product_public_ID=9090909,
            name='Шорты',
            description='Шорты Класические',
            price='100.00'
        )
        image_path = 'fixtures_data/archive/CUCCI/img1.jpg'
        image = SimpleUploadedFile(
            name='img1',
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg'
        )

        ProductImage.objects.create(title='image-1', description='description-1', image=image, product=product)
        ProductImage.objects.create(title='', description='', image=image, product=product)

    def test_object_str_1(self):
        obj = ProductImage.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'image-1 ID: 9090909 NAME: Шорты')

    def test_object_str_2(self):
        obj = ProductImage.objects.get(id=2)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'нет заголовка ID: 9090909 NAME: Шорты')


class CartModelsTest(TestCase):
    """Shop.models.Cart"""

    def test_product_cost_1(self):
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=100.00)
        obj = Cart.objects.create(user=User.objects.create(username='admin'), product=card, total=1)
        expected_object_name = '%s' % str(obj.product_cost)
        self.assertEquals(expected_object_name, '100.0')

    def test_product_cost_2(self):
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=444.44)
        obj = Cart.objects.create(user=User.objects.create(username='admin'), product=card, total=4)
        expected_object_name = '%s' % str(obj.product_cost)
        self.assertEquals(expected_object_name, '1777.76')

    def test_product_cost_3(self):
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=0)
        obj = Cart.objects.create(user=User.objects.create(username='admin'), product=card, total=1)
        expected_object_name = '%s' % str(obj.product_cost)
        self.assertEquals(expected_object_name, '0')

    def test_object_str(self):
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=1)
        obj = Cart.objects.create(user=User.objects.create(username='admin'), product=card, total=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'ID: 999991 NAME: name, admin')

    def test_total_price(self):
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=1)
        obj = Cart.objects.create(user=User.objects.create(username='admin'), product=card, total=1)
        expected_object_name = '%s' % str(obj.total_price(1))
        self.assertEquals(expected_object_name, '1')


class FavoritesModelsTest(TestCase):
    """Shop.models.Favorites"""

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='admin')
        card = Card_Product.objects.create(product_public_ID=999991, name='name', description='des', price=1)
        Favorites.objects.create(user=user, products=card)

    def test_object_str(self):
        obj = Favorites.objects.get(id=1)
        expected_object_name = '%s' % str(obj)
        self.assertEquals(expected_object_name, 'admin, ID: 999991 NAME: name')
