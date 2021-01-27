from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
User=get_user_model()


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to=kwargs.get('whith_respect_to')
        products=[]
        ct_models=ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products=ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model=ContentType.objects.filter(model=with_respect_to)
            if ct_model.exist():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
                ct_model=ct_model.first()
        return products


class LatestProducts:
   
    objects=LatestProductsManager()


class Category(models.Model):

    name=models.CharField(max_length=255, verbose_name='Имя катергории')
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    class Meta:
        abstract =True

    category=models.ForeignKey(Category, verbose_name='Категория',on_delete=models.CASCADE)
    title=models.CharField(max_length=255, verbose_name='Наименование')
    slug=models.SlugField(unique=True)
    image=models.ImageField()
    description=models.TextField()
    price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class CardProduct(models.Model):

    user=models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    card=models.ForeignKey('Card', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_objct=GenericForeignKey('content_type', 'object_id')
    qty=models.PositiveIntegerField(default=1)
    final_price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукут: {self.product.title} (для корзины)'

        
class Card(models.Model):

    owner=models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    product=models.ManyToManyField(CardProduct, blank=True, related_name='related_card')
    total_products=models.PositiveIntegerField(default=0)
    final_price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user=models.ForeignKey(User, verbose_name='Пользовотель', on_delete=models.CASCADE)
    #first_name=models.CharField(max_length=255,verbose_name='Имя пользователя')
    phone=models.CharField(max_length=20, verbose_name='Номер телефона')
    address=models.CharField(max_length=255, verbose_name='Адрес')

    def __str__ (self):
        return f'Покупатель: {self.user.first_name} {self.user.last_name}'


class Notebook(Product):

    diagonal=models.CharField(max_length=255, verbose_name='Диагональ')
    display_type=models.CharField(max_length=255, verbose_name='Тип дисплея')
    procesessor_freq=models.CharField(max_length=255, verbose_name='Частота процессора')
    ram=models.CharField(max_length=255, verbose_name='Оперативная память')
    video=models.CharField(max_length=255, verbose_name='Видео карта')
    time_without_charge=models.CharField(max_length=255, verbose_name='Вермя работы аккамулятора')

    def __str__(self):
        return f'{self.category.name}:{self.title}'

class Smartphone(Product):
    diagonal=models.CharField(max_length=255, verbose_name='Диагональ')
    display_type=models.CharField(max_length=255, verbose_name='Тип дисплея')
    resulution=models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume=models.CharField(max_length=255, verbose_name='Обьем батареи')
    ram=models.CharField(max_length=255, verbose_name='Оперативная память')
    sd=models.BooleanField(default=True)
    sd_volume_max=models.CharField(max_length=255, verbose_name='Максимальный обьем встраиваимой памяти')
    main_cam_mp=models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp=models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return f'{self.category.name}:{self.title}'

# class Specifications(models.Model):

#     cont_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id=models.PositiveIntegerField()
#     name=models.CharField(max_length=255, verbose_name='Имя товара для характеристик')

#     def __str__(self):
#         return f'Характеристик для товара: {self.name}'