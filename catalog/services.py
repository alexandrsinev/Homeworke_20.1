from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_version_from_cache(product_pk):
    """Функция получает данные по версиям продукта. Если кеширование отключено данные получаются из БД, в обратном
    случае проверяется есть ли данные в кеше, если есть возвращаются из кеша, если нет берутся из БД предварительно
    сохраняются в кеш"""
    if not CACHE_ENABLED:
        version_list = Product.objects.filter(produkt_pk=product_pk)
        return version_list
    key = f'version_list_{product_pk}'
    version_list = cache.get(key)
    if version_list is not None:
        return version_list
    version_list = Product.objects.filter(produkt_pk=product_pk)
    cache.set(key, version_list)
    return version_list
