from django.urls import reverse
from django.db import models


class Bulletin(models.Model):
	title = models.CharField(max_length=50, verbose_name='Заголовок')
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
	content = models.TextField(blank=True, verbose_name='Описание')
	photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
	price = models.FloatField(null=True, blank=True, verbose_name='Цена')
	time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время создания')
	time_update = models.DateTimeField(auto_now=True, verbose_name='Дата/время изменения')
	is_published = models.BooleanField(default=True, verbose_name='Публикация')
	cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post', kwargs={'post_slug': self.slug})

	def get_price(self):
		return f"{int(self.price):_} ₽".replace("_", " ")

	class Meta:
		verbose_name = 'Объявления'
		verbose_name_plural = 'Объявления'
		ordering = ['-time_create']


class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category', kwargs={'cat_slug': self.slug})

	class Meta:
		verbose_name = 'Категории'
		verbose_name_plural = 'Категории'
		ordering = ['id']
