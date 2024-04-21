import json

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        # Здесь мы получаем данные из фикстур с категориями
        with open('catalog_data.json') as file:
            list_of_fixture = json.load(file)
            list_category = []
            for item in list_of_fixture:
                if item['model'] == 'catalog.category':
                    list_category.append(item['fields'])

        return list_category

    @staticmethod
    def json_read_products():
        # Здесь мы получаем данные из фикстур с продуктами
        with open('catalog_data.json') as file:
            list_of_fixture = json.load(file)
            list_product = []
            for item in list_of_fixture:
                if item['model'] == 'catalog.product':
                    list_product.append(item['fields'])
        return list_product

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создаем списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(Category(**category))

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(name=product['name'], description=product['description'],
                        photo=product['photo'],
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product['category']), price=product['price'],
                        created_at=product['created_at'], updated_at=product['updated_at'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
